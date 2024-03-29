import datetime
from app.utils.uuid import generate_uuid
from app.schemas.tag import TagBase, UpdateTagData
from app.database.models.Product import Tag
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def is_exist_name(name: str, db: AsyncSession) -> UUID | None:
    result = await db.execute(
        select(Tag.id).where(Tag.name == name).where(Tag.deleted_at.is_(None))
    )
    return result.scalars().first()


async def is_exist_name_delete(name: str, db: AsyncSession) -> UUID | None:
    result = await db.execute(
        select(Tag.id).where(Tag.name == name).where(Tag.deleted_at.isnot(None))
    )
    return result.scalars().first()


async def get_tag_by_id(id: UUID, db: AsyncSession) -> Tag | None:
    result = await db.execute(
        select(Tag).where(Tag.id == id).where(Tag.deleted_at.is_(None))
    )
    return result.scalars().first()


async def create(data: TagBase, db: AsyncSession):
    id = generate_uuid()
    tag = await is_exist_name_delete(data.name, db)

    # if tag is exist, then update the tag
    if tag:
        await db.execute(update(Tag).where(Tag.id == tag).values(deleted_at=None))
        await db.commit()
        return

    # if tag is not exist, then create the tag
    db_tag = Tag(id=id, **data.model_dump())
    db.add(db_tag)
    await db.commit()
    pass


async def update_tag(id: UUID, data: UpdateTagData, db: AsyncSession):
    await db.execute(update(Tag).where(Tag.id == id).values(**data.model_dump()))
    await db.commit()


async def delete_tag(id: UUID, db: AsyncSession):
    await db.execute(
        update(Tag).where(Tag.id == id).values(deleted_at=datetime.datetime.now())
    )
    await db.commit()


async def get_all(db: AsyncSession):
    list_tag = await db.execute(select(Tag).where(Tag.deleted_at.is_(None)))
    return list_tag.scalars().all()


async def get_tag_id_by_name(name: UUID, db: AsyncSession):
    result = await db.execute(select(Tag.id).where(Tag.name == name))
    return result.scalars().first()
