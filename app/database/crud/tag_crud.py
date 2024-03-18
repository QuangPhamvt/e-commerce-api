from app.utils.uuid import generate_uuid
from app.schemas.tag import CreateTagData, UpdateTagData
from app.database.models.Product import Tag
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


async def is_exist_name(name: str, db: AsyncSession) -> UUID | None:
    result = await db.execute(select(Tag.id).where(Tag.name == name))
    return result.scalars().first()


async def get_tag_by_id(id: UUID, db: AsyncSession) -> Tag | None:
    result = await db.execute(select(Tag).where(Tag.id == id))
    return result.scalars().first()


async def create(data: CreateTagData, db: AsyncSession):
    id = generate_uuid()
    db_tag = Tag(id=id, **data.model_dump())
    db.add(db_tag)
    await db.commit()


async def update_tag(id: UUID, data: UpdateTagData, db: AsyncSession):
    await db.execute(update(Tag).where(Tag.id == id).values(**data.model_dump()))
    await db.commit()


async def delete_tag(id: UUID, db: AsyncSession):
    await db.execute(delete(Tag).where(Tag.id == id))
    await db.commit()


async def get_all(db: AsyncSession):
    list_tag = await db.execute(select(Tag))
    return list_tag.scalars().all()
