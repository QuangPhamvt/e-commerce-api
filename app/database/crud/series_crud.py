from datetime import datetime
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from app.database.models.Product import Series
from app.schemas.series import CreateSeriesData, UpdateSeriesData
from app.utils.uuid import generate_uuid


async def get_series_by_name(name: str, db: AsyncSession) -> UUID | None:
    result = await db.execute(select(Series.id).where(Series.name == name))
    return result.scalars().first()


async def get_series_by_id(id: UUID, db: AsyncSession) -> Series | None:
    result = await db.execute(select(Series).where(Series.id == id))
    return result.scalars().first()


async def create(data: CreateSeriesData, db: AsyncSession):
    id = generate_uuid()
    db_series = Series(id=id, **data.model_dump())
    db.add(db_series)
    await db.commit()


async def update_series(id: UUID, data: UpdateSeriesData, db: AsyncSession):
    await db.execute(
        update(Series)
        .where(Series.id == id)
        .values(**data.model_dump(), updated_at=datetime.today())
    )
    await db.commit()


async def delete_series(id: UUID, db: AsyncSession):
    await db.execute(delete(Series).where(Series.id == id))
    await db.commit()


async def get_all(db: AsyncSession):
    list_series = await db.execute(
        select(Series).options(
            defer(Series.created_at),
            defer(Series.updated_at),
        )
    )
    return list_series.scalars().all()
