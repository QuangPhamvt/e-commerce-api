from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database.crud.cart_crud import CartCRUD
from app.database.crud.product_crud import ProductCRUD
from app.schemas.cart import CreateCartData, CreateCartParam


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cart_crud = CartCRUD(db)
        self.product_crud = ProductCRUD(db)

    async def create(self, body: CreateCartParam, user_id: UUID):
        is_exist_product = await self.product_crud.read_by_id(body.product_id)
        if not is_exist_product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product Not Found")
        await self.cart_crud.create_cart(
            CreateCartData(user_id=user_id, **body.model_dump())
        )
        return {"detail": "Add Product to Cart Succeed!"}

    async def read_by_user(self, user_id: UUID):
        return await self.cart_crud.read_by_user_id(user_id)

    async def delete(self, id: UUID, user_id: UUID):
        is_exist_cart = await self.cart_crud.read_by_id(id, user_id)
        if not is_exist_cart:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cart Not Found")
        await self.cart_crud.delete_cart(id)
        return {"detail": "Delete Cart Succeed!"}
