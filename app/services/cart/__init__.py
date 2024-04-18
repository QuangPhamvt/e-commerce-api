import logging
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database.crud.cart_crud import CartCRUD
from app.database.crud.product_crud import ProductCRUD
from app.schemas.cart import CreateCartData, CreateCartParam


class CartService:
    """
    Cart Service
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.cart_crud = CartCRUD(db)
        self.product_crud = ProductCRUD(db)

    async def create(self, body: CreateCartParam, user_id: UUID):
        is_exist_product = await self.product_crud.read_by_id(body.product_id)
        if not is_exist_product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product Not Found")
        try:
            is_exist_cart = await self.cart_crud.read_by_user_and_product(
                user_id, body.product_id
            )
            if is_exist_cart:
                await self.cart_crud.update_quantity(
                    is_exist_cart.id, body.quantity + is_exist_cart.quantity
                )
            else:
                await self.cart_crud.create_cart(
                    CreateCartData(user_id=user_id, **body.model_dump())
                )
        except Exception as e:
            logging.warning(f"Error reading cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to read cart")

        return {"detail": "Add Product to Cart Succeed!"}

    async def read_by_user(self, user_id: UUID):
        try:
            carts = await self.cart_crud.read_by_user_id(user_id)
            result = []
            for cart in carts:
                product = await self.product_crud.read_by_id(cart.product_id)
                if product:
                    product.__dict__.pop("original_price")
                    product.__dict__.pop("created_at")
                    product.__dict__.pop("updated_at")
                    product.__dict__.pop("deleted_at")
                cart.__dict__.pop("product_id")
                cart.__dict__.pop("user_id")
                result.append({**cart.__dict__, "product": product.__dict__})
            return result
        except Exception as e:
            logging.warning(f"Error reading database : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to read cart")

    async def delete(self, id: UUID, user_id: UUID):
        is_exist_cart = await self.cart_crud.read_by_id(id, user_id)
        if not is_exist_cart:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cart Not Found")
        try:
            await self.cart_crud.delete_cart(id)
        except Exception as e:
            logging.warning(f"Error delete cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to delete cart")
        return {"detail": "Delete Cart Succeed!"}
