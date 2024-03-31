import logging
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import defer
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_tag_crud import ProductTagCRUD
from app.database.models import Product
from app.utils.helper import helper
from app.utils.uuid import generate_uuid
from app.schemas.product import BodyUpdateProduct, ProductCreateCRUD


class ProductCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_tag_crud = ProductTagCRUD(db)

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
        except Exception as e:
            logging.warning(f"Error creating product : {e}")
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to create product")

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
                .options(
                    defer(Product.series_id),
                )
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
        if data["name"]:
            data["slug"] = helper.slugify(data["name"])
        await self.db.execute(update(Product).where(Product.id == id).values(data))
        await self.db.commit()

    async def delete_by_id(self, id: UUID) -> None:
        await self.db.execute(delete(Product).where(Product.id == id))
        await self.product_tag_crud.delete_by_product_id(id)
        await self.db.commit()
