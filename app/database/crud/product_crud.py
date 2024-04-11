from uuid import UUID
from sqlalchemy.orm import defer
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Product, product_tag
from app.utils.helper import helper
from app.utils.uuid import generate_uuid
from app.schemas.product import BodyUpdateProduct, ProductCreateCRUD


class ProductCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product: ProductCreateCRUD) -> UUID:
        db = self.db
        uuid = generate_uuid()

        db_product = Product(
            id=uuid,
            **product.model_dump(exclude={"thumbnail_type", "tags"}),
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
        return (
            (
                await self.db.execute(
                    select(Product)
                    .where(Product.id == id)
                    .where(Product.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

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
        await self.db.execute(
            product_tag.delete().where(product_tag.c.product_id == id)
        )
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

    async def read_product_slug(self, id: UUID):
        return (
            (await self.db.execute(select(Product.slug).where(Product.id == id)))
            .scalars()
            .first()
        )
