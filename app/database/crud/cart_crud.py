from datetime import datetime
import logging
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from app.database.crud.product_crud import ProductCRUD
from app.database.models import Cart
from app.schemas.cart import CreateCartData
from app.utils.uuid import generate_uuid

"""
CART CRUD
"""


class CartCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_crud = ProductCRUD(db)

    async def read_by_user_and_product(self, user_id: UUID, product_id: UUID):
        try:
            cart = await self.db.execute(
                select(Cart).where(
                    Cart.user_id == user_id, Cart.product_id == product_id
                )
            )
            return cart.scalars().first()
        except Exception as e:
            logging.warning(f"Error reading cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to read cart")

    async def create_cart(self, data: CreateCartData):
        try:
            exist_cart = await self.read_by_user_and_product(
                data.user_id, data.product_id
            )
            if not exist_cart:
                id = generate_uuid()
                cart = Cart(id, **data.model_dump())
                self.db.add(cart)
            else:
                await self.db.execute(
                    update(Cart)
                    .where(Cart.id == exist_cart.id)
                    .values(
                        quantity=exist_cart.quantity + data.quantity,
                        updated_at=datetime.today(),
                    )
                )

            await self.db.commit()
        except Exception as e:
            logging.warning(f"Error creating cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create cart")

    async def read_by_user_id(self, user_id: UUID):
        try:
            carts = await self.db.execute(
                select(Cart)
                .where(Cart.user_id == user_id)
                .options(
                    defer(Cart.created_at),
                    defer(Cart.updated_at),
                )
            )
            results = [
                {
                    **cart.Cart.asdict(),
                    "product": await self.product_crud.read_by_id(cart.Cart.product_id),
                }
                for cart in carts.mappings()
            ]
            return results
        except Exception as e:
            logging.warning(f"Error reading cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to read carts")

    async def delete_cart(self, cart_id: UUID):
        try:
            await self.db.execute(delete(Cart).where(Cart.id == cart_id))
            await self.db.commit()
        except Exception as e:
            logging.warning(f"Error deleting cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to delete cart")

    async def read_by_id(self, cart_id: UUID, user_id: UUID):
        try:
            cart = await self.db.execute(
                select(Cart).where(Cart.id == cart_id).where(Cart.user_id == user_id)
            )
            return cart.scalars().first()
        except Exception as e:
            logging.warning(f"Error reading cart : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to read cart")
