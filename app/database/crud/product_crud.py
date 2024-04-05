import logging
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import defer
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_tag_crud import ProductTagCRUD
from app.database.models import (
    Product,
    Category,
    Series,
)
from app.utils.helper import helper
from app.utils.uuid import generate_uuid
from app.schemas.product import BodyUpdateProduct, ProductCreateCRUD


class ProductCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_tag_crud = ProductTagCRUD(db)

    async def create(self, product: ProductCreateCRUD) -> UUID:
        db = self.db
        uuid = generate_uuid()
        series_id = product.series_id
        category_id = product.category_id

        old_product = await self.read_by_slug(product.slug)

        series_id = (
            (await db.execute(select(Series.id).where(Series.id.__eq__(series_id))))
            .scalars()
            .first()
        )
        category_id = (
            (
                await db.execute(
                    select(Category.id).where(Category.id.__eq__(category_id))
                )
            )
            .scalars()
            .first()
        )

        # Check if series_id and category_id exist and product not exist
        if not series_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series id not found")
        if not category_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category id not found")
        if old_product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product already exist")

        db_product = Product(
            id=uuid,
            series_id=series_id,
            category_id=category_id,
            **product.model_dump(
                exclude={"thumbnail_type", "tags", "series_id", "category_id"}
            ),
        )
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return uuid

    async def read_all(self):
        return (
            (
                await self.db.execute(
                    select(Product)
                    .options(
                        defer(Product.created_at),
                        defer(Product.updated_at),
                        defer(Product.deleted_at),
                    )
                    .where(Product.deleted_at.is_(None))
                )
            )
            .scalars()
            .all()
        )

    async def read_by_id(self, id: UUID) -> Product | None:
        try:
            product = await self.db.execute(
                select(Product)
                .where(Product.id == id)
                .where(Product.deleted_at.is_(None))
            )
            return product.scalars().first()
        except Exception as e:
            logging.warning(f"Error getting product by id : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to get product")

    async def read_by_slug(self, slug: str) -> Product | None:
        return (
            (
                await self.db.execute(
                    select(Product)
                    .where(Product.slug == slug)
                    .where(Product.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def update_by_id(self, id: UUID, product: BodyUpdateProduct) -> None:
        data = {k: v for k, v in product.model_dump().items() if v is not None}
        if data["name"] is not None:
            data["slug"] = helper.slugify(data["name"])
        await self.db.execute(update(Product).where(Product.id == id).values(data))
        await self.db.commit()

    async def delete_by_id(self, id: UUID) -> None:
        await self.product_tag_crud.delete_by_product_id(id)
        await self.db.execute(delete(Product).where(Product.id == id))
        await self.db.commit()

    async def update_series_to_product(self, product_id: UUID, series_id: UUID) -> None:
        await self.db.execute(
            update(Product).where(Product.id == product_id).values(series_id=series_id)
        )
        await self.db.commit()

    async def update_category_to_product(
        self, product_id: UUID, category_id: UUID
    ) -> None:
        await self.db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(category_id=category_id)
        )
        await self.db.commit()

    async def read_product_by_series(self, series_id: UUID):
        return (
            (
                await self.db.execute(
                    select(Product)
                    .where(Product.series_id == series_id)
                    .where(Product.deleted_at.is_(None))
                    .options(
                        defer(Product.created_at),
                        defer(Product.updated_at),
                        defer(Product.deleted_at),
                    )
                )
            )
            .scalars()
            .all()
        )
