from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import defer
from app.database.models.Product import Tag, product_tag, Product


class ProductTagCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product_id: UUID, tag_id: UUID):
        await self.db.execute(
            product_tag.insert().values(product_id=product_id, tag_id=tag_id)
        )
        await self.db.commit()

    async def create_many_by_product_id(self, product_id: UUID, tags: list[UUID]):
        values = [{"product_id": product_id, "tag_id": tag_id} for tag_id in tags]
        exist_tags = (
            (
                await self.db.execute(
                    select(product_tag)
                    .where(product_tag.c.product_id == product_id)
                    .where(product_tag.c.tag_id.in_([tag_id for tag_id in tags]))
                )
            )
            .scalars()
            .all()
        )
        values = [
            value
            for value in values
            if not any([value["tag_id"] == exist.tag_id for exist in exist_tags])
        ]
        await self.db.execute(product_tag.insert().values(values))
        await self.db.commit()

    async def is_exist(self, product_id: UUID, tag_id: UUID):
        return (
            (
                await self.db.execute(
                    select(product_tag)
                    .where(product_tag.c.product_id == product_id)
                    .where(product_tag.c.tag_id == tag_id)
                )
            )
            .scalars()
            .first()
        )

    async def read_by_tag(self, tag_id: UUID):
        return (
            (
                await self.db.execute(
                    select(Product)
                    .select_from(product_tag)
                    .join(Product, product_tag.c.product_id == Product.id)
                    .where(product_tag.c.tag_id == tag_id)
                )
            )
            .scalars()
            .all()
        )

    async def read_list_tags_by_product(self, product_id: UUID):
        return (
            (
                await self.db.execute(
                    select(Tag)
                    .options(
                        defer(Tag.deleted_at),
                    )
                    .select_from(product_tag)
                    .join(Tag, product_tag.c.tag_id == Tag.id)
                    .where(product_tag.c.product_id == product_id)
                    .where(Tag.deleted_at.is_(None))
                )
            )
            .scalars()
            .all()
        )

    async def delete_by_tag_id(self, tag_id: UUID):
        await self.db.execute(
            product_tag.delete().where(product_tag.c.tag_id == tag_id)
        )
        await self.db.commit()

    async def delete_by_product_id(self, product_id: UUID):
        await self.db.execute(
            product_tag.delete().where(product_tag.c.product_id == product_id)
        )
        await self.db.commit()
