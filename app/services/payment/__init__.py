from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from operator import itemgetter
from app.configs.payos import PayOSApi
from app.database.crud import deposit_crud
from app.database.crud.bill_crud import BillCRUD
from app.database.crud.cart_crud import CartCRUD
from app.database.crud.product_crud import ProductCRUD
from app.schemas.bill import (
    CreateBillBody,
    CreateBillData,
    CreateBillDetailBody,
    CreateBillDetailData,
    ProductBillInfo,
    StatusEnum,
)
from app.schemas.payos import BillData, ProductData
from app.utils.uuid import generate_current_timestamp, generate_uuid


class PaymentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cart_crud = CartCRUD(db)
        self.bill_crud = BillCRUD(db)
        self.product_crud = ProductCRUD(db)
        self.cart_crud = CartCRUD(db)

    async def checkout(self, body: CreateBillBody, user_id: UUID):
        details = body.details
        list_product_id = [detail.product_id for detail in details]
        list_product = await self.product_crud.read_by_list_id(list_product_id)
        list_product_info = [
            ProductBillInfo(id=product.id, name=product.name, quantity=product.quantity)
            for product in list_product
        ]
        if len(list_product) != len(list_product_id):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Some product not found")
        # check quantity and decrease quantity in product
        await self.__decrease_product_quantity(list_product_info, details)
        # Delete cart
        await self.cart_crud.delete_cart(user_id, list_product_id)
        if not body.deposit_type_id:
            return await self.__handle_ship_cod(body, user_id)
        try:
            # Create bill
            payos_id = await self.__create_bill(body, user_id)
            # Create payment link
            (
                product_price,
                customer_address,
                customer_province,
                customer_district,
                customer_ward,
                customer_fullname,
                customer_phone_number,
            ) = itemgetter(
                "product_price",
                "customer_address",
                "customer_province",
                "customer_district",
                "customer_ward",
                "customer_fullname",
                "customer_phone_number",
            )(body.model_dump())
            full_address = ", ".join(
                [customer_address, customer_ward, customer_district, customer_province]
            )

            deposit_type = await deposit_crud.get_deposit_type_by_id(
                body.deposit_type_id, self.db
            )
            if not deposit_type:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Deposit type not found"
                )
            product_price = (
                product_price * deposit_type.value + product_price * deposit_type.fee
            )
            payment_bill_data = BillData(
                orderCode=payos_id,
                amount=int(product_price),
                description="",
                buyerAddress=full_address,
                buyerEmail="",
                buyerName=customer_fullname,
                buyerPhone=customer_phone_number,
            )
            payment_product_data: list[ProductData] = []
            for detail in details:
                name = ""
                for product in list_product_info:
                    if product.id == detail.product_id:
                        name = product.name
                product_data = ProductData(
                    quantity=detail.quantity, price=int(detail.price), name=name
                )
                payment_product_data.append(product_data)
            payment_link_data = await PayOSApi.create_payment_link(
                payment_product_data, payment_bill_data
            )
            return {
                "detail": "Checkout Succeed!",
                "checkout_url": payment_link_data.get("checkoutUrl")
                if payment_link_data
                else None,
            }

        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    async def __handle_ship_cod(self, body: CreateBillBody, user_id: UUID):
        try:
            await self.__create_bill(body, user_id)
            return {"detail": "Checkout Succeed!"}
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    async def payment_success(self, order_code: int):
        await self.__is_valid_order_code(order_code)
        await self.bill_crud.update_bill_status_by_order_code(
            order_code, StatusEnum.PROCESSING
        )
        return {"detail": "Payment success!. Your bill is being processed"}

    async def payment_fail(self, order_code: int):
        await self.__is_valid_order_code(order_code)
        await self.bill_crud.update_bill_status_by_order_code(
            order_code, StatusEnum.CANCELED
        )
        return {"detail": "Payment fail!. Your bill is canceled"}

    async def __is_valid_order_code(self, order_code: int):
        bill = await self.bill_crud.read_by_order_code(order_code)
        if not bill:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Bill not found!")

    async def __create_bill(self, body: CreateBillBody, user_id: UUID):
        details = body.details
        data_bill = CreateBillData(
            **body.model_dump(), user_id=user_id, status=StatusEnum.PENDING
        )
        bill_id = generate_uuid()
        payos_id = generate_current_timestamp()
        bill_details_data: list[CreateBillDetailData] = []
        for detail in details:
            bill_details_data.append(
                CreateBillDetailData(**detail.model_dump(), bill_id=bill_id)
            )
        await self.bill_crud.create_bill(data_bill, bill_id, payos_id)
        await self.bill_crud.create_bill_detail(bill_details_data)
        return payos_id

    async def __decrease_product_quantity(
        self,
        list_product_info: list[ProductBillInfo],
        details: list[CreateBillDetailBody],
    ):
        for detail in details:
            for product in list_product_info:
                if product.id == detail.product_id:
                    if product.quantity < detail.quantity:
                        raise HTTPException(
                            status.HTTP_400_BAD_REQUEST,
                            f"Product {product.name} is out of stock. Please select lower quantity",
                        )
                    product.quantity -= detail.quantity
        await self.product_crud.update_quantity(list_product_info)
