from datetime import datetime
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from app.database.models import Cart
from app.schemas.cart import CreateCartData
from app.utils.uuid import generate_uuid


class CartCRUD:
    """
    CART CRUD

    This file is used to interact with the cart database.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def read_by_user_and_product(self, user_id: UUID, product_id: UUID):
        cart = await self.db.execute(
            select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
        )
        return cart.scalars().first()

    async def create_cart(self, data: CreateCartData):
        id = generate_uuid()
        cart = Cart(id, **data.model_dump())
        self.db.add(cart)
        await self.db.commit()
        return

    async def update_quantity(self, id: UUID, quantity: int):
        await self.db.execute(
            update(Cart)
            .where(Cart.id == id)
            .values(quantity=quantity, updated_at=datetime.today())
        )
        await self.db.commit()
        return

    async def read_by_user_id(self, user_id: UUID):
        return (
            (
                await self.db.execute(
                    select(Cart)
                    .where(Cart.user_id == user_id)
                    .options(
                        defer(Cart.created_at),
                        defer(Cart.updated_at),
                    )
                )
            )
            .scalars()
            .all()
        )

    async def delete_cart(self, user_id: UUID, list_product_id: list[UUID]):
        await self.db.execute(
            delete(Cart)
            .where(Cart.user_id == user_id)
            .where(Cart.product_id.in_(list_product_id))
        )
        await self.db.commit()

    async def read_by_id(self, cart_id: UUID, user_id: UUID):
        cart = await self.db.execute(
            select(Cart).where(Cart.id == cart_id).where(Cart.user_id == user_id)
        )
        return cart.scalars().first()
