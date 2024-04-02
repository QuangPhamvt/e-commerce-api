import datetime
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_tag_crud import ProductTagCRUD

from app.utils.uuid import generate_uuid
from app.schemas.tag import TagBase, UpdateTagData
from app.database.models.Product import Tag


class TagCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_tag_crud = ProductTagCRUD(db)

    async def is_exist_name(self, name: str) -> UUID | None:
        return (
            (
                await self.db.execute(
                    select(Tag.id)
                    .where(Tag.name == name)
                    .where(Tag.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def is_exist_name_delete(self, name: str) -> UUID | None:
        return (
            (
                await self.db.execute(
                    select(Tag.id)
                    .where(Tag.name == name)
                    .where(Tag.deleted_at.isnot(None))
                )
            )
            .scalars()
            .first()
        )

    async def read_by_id(self, id: UUID) -> Tag | None:
        return (
            (
                await self.db.execute(
                    select(Tag).where(Tag.id == id).where(Tag.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def create(self, data: TagBase):
        id = generate_uuid()
        tag = await self.is_exist_name_delete(data.name)

        # if tag is exist, then update the tag
        if tag:
            await self.db.execute(
                update(Tag).where(Tag.id == tag).values(deleted_at=None)
            )
            await self.db.commit()
            return

        # if tag is not exist, then create the tag
        db_tag = Tag(id=id, **data.model_dump())
        self.db.add(db_tag)
        await self.db.commit()

    async def read_all(self):
        return (
            (await self.db.execute(select(Tag).where(Tag.deleted_at.is_(None))))
            .scalars()
            .all()
        )

    async def read_all_name(self):
        return (
            (await self.db.execute(select(Tag.name).where(Tag.deleted_at.is_(None))))
            .scalars()
            .all()
        )

    async def read_by_name(self, name: str):
        return (
            (await self.db.execute(select(Tag.id).where(Tag.name == name)))
            .scalars()
            .first()
        )

    async def update(self, id: UUID, data: UpdateTagData):
        await self.db.execute(
            update(Tag).where(Tag.id == id).values(**data.model_dump())
        )
        await self.db.commit()

    async def delete(self, id: UUID):
        await self.db.execute(
            update(Tag).where(Tag.id == id).values(deleted_at=datetime.datetime.now())
        )
        await self.product_tag_crud.delete_by_tag_id(id)
        await self.db.commit()
