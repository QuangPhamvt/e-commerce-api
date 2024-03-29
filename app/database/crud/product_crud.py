import logging
import datetime
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import defer
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Product
from app.utils.uuid import generate_uuid
from app.schemas.product import BodyUpdateProduct, ProductCreateCRUD


class ProductCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product: ProductCreateCRUD) -> None:
        try:
            db = self.db
            uuid = generate_uuid()
            db_product = Product(
                id=uuid,
                category_id=None,
                **product.model_dump(exclude={"thumbnail_type"}),
            )
            db.add(db_product)
            await db.commit()
            await db.refresh(db_product)
            pass
        except Exception as e:
            logging.warning(f"Error creating product : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create product")

    async def get_products(self):
        db = self.db
        products = await db.execute(
            select(Product)
            .options(
                defer(Product.created_at),
                defer(Product.updated_at),
            )
            .where(Product.deleted_at.is_(None))
        )
        return products.scalars().all()

    async def get_product_by_id(self, id: UUID) -> Product | None:
        db = self.db
        try:
            product = await db.execute(
                select(Product)
                .options(
                    defer(Product.deleted_at),
                    defer(Product.series_id),
                    defer(Product.category_id),
                    defer(Product.created_at),
                    defer(Product.updated_at),
                )
                .where(Product.id == id)
                .where(Product.deleted_at.is_(None))
            )
            return product.scalars().first()
        except Exception as e:
            logging.warning(f"Error getting product by id : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to get product")

    async def get_product_by_slug(self, slug: str) -> Product | None:
        db = self.db
        product = await db.execute(
            select(Product)
            .where(Product.slug == slug)
            .where(Product.deleted_at.is_(None))
        )
        return product.scalars().first()

    async def delete_by_id(self, id: UUID) -> None:
        db = self.db
        await db.execute(
            update(Product)
            .where(Product.id == id)
            .values(deleted_at=datetime.datetime.now())
        )
        await db.commit()
        pass

    async def update_by_id(self, id: UUID, product: BodyUpdateProduct) -> None:
        db = self.db
        data = {k: v for k, v in product.model_dump().items() if v is not None}
        await db.execute(update(Product).where(Product.id == id).values(data))
        await db.commit()
        pass
