from uuid import UUID
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.Product import ProductsImage
from app.schemas.product import CreateProductsImageBody
from app.utils.uuid import generate_uuid
from sqlalchemy.orm import defer


class ProductsImageCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, body: CreateProductsImageBody):
        db = self.db
        uuid = generate_uuid()
        db_image = ProductsImage(id=uuid, **body.model_dump())
        db.add(db_image)
        await db.commit()
        await db.refresh(db_image)

    async def delete(self, id: UUID):
        await self.db.execute(delete(ProductsImage).where(ProductsImage.id == id))
        await self.db.commit()

    async def get_product_image_id_by_slug(self, slug: str):
        return (
            (
                await self.db.execute(
                    select(ProductsImage.id).where(ProductsImage.slug == slug)
                )
            )
            .scalars()
            .first()
        )

    async def update(self, id: UUID, image_slug: str, image_url: str):
        await self.db.execute(
            update(ProductsImage)
            .where(ProductsImage.id == id)
            .values(slug=image_slug, image_url=image_url)
        )
        await self.db.commit()

    async def images_quantity(self, id: UUID):
        return (
            (
                await self.db.execute(
                    select(func.count()).where(ProductsImage.product_id == id)
                )
            )
            .scalars()
            .first()
        )

    async def get_list_image_urls(self, id: UUID):
        return (
            (
                await self.db.execute(
                    select(ProductsImage.image_url).where(
                        ProductsImage.product_id == id
                    )
                )
            )
            .scalars()
            .all()
        )

    async def get_product_images(self, id: UUID):
        return (
            (
                await self.db.execute(
                    select(ProductsImage)
                    .options(
                        defer(ProductsImage.id),
                        defer(ProductsImage.product_id),
                        defer(ProductsImage.created_at),
                        defer(ProductsImage.updated_at),
                        defer(ProductsImage.deleted_at),
                    )
                    .where(ProductsImage.product_id == id)
                    .where(ProductsImage.deleted_at.is_(None))
                )
            )
            .scalars()
            .all()
        )

    async def delete_by_product_id(self, id: UUID):
        await self.db.execute(
            delete(ProductsImage).where(ProductsImage.product_id == id)
        )
        await self.db.commit()
