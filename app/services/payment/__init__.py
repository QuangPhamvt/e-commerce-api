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
    CreateBillDetailData,
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
        cart = await self.cart_crud.read_by_id(body.cart_id, user_id)

        if not cart:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cart not found")
        product_id = cart.product_id
        try:
            detail = body.detail
            # Create bill
            payos_id = await self.__create_bill(body, user_id, product_id)
            # Delete cart
            await self.cart_crud.delete_cart(body.cart_id)
            # Create payment link
            product = await self.product_crud.read_by_id(product_id)

            if not product:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found")
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
            if body.deposit_type_id:
                deposit_type = await deposit_crud.get_deposit_type_by_id(
                    body.deposit_type_id, self.db
                )
                if not deposit_type:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, "Deposit type not found"
                    )
                product_price = (
                    product_price * deposit_type.value
                    + product_price * deposit_type.fee
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
            payment_product_data = ProductData(
                name=product.name,
                quantity=detail.quantity,
                price=int(detail.price),
            )
            payment_link_data = await PayOSApi.create_payment_link(
                payment_product_data, payment_bill_data
            )
            return {"detail": "Checkout Succeed!", "data": payment_link_data}

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

    async def __create_bill(
        self, body: CreateBillBody, user_id: UUID, product_id: UUID
    ):
        detail = body.detail
        data_bill = CreateBillData(
            **body.model_dump(), user_id=user_id, status=StatusEnum.PENDING
        )
        bill_id = generate_uuid()
        payos_id = generate_current_timestamp()
        await self.bill_crud.create_bill(data_bill, bill_id, payos_id)
        data_bill_detail = CreateBillDetailData(
            **detail.model_dump(), bill_id=bill_id, product_id=product_id
        )
        await self.bill_crud.create_bill_detail(data_bill_detail)
        return payos_id
