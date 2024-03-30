import datetime
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from app.database.models.Product import Series
from app.schemas.series import CreateSeriesCRUD, UpdateSeriesById
from app.utils.uuid import generate_uuid


class SeriesCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def is_exist_name(self, name: str) -> UUID | None:
        return (
            (
                await self.db.execute(
                    select(Series.id)
                    .where(Series.deleted_at.is_(None))
                    .where(Series.name == name)
                )
            )
            .scalars()
            .first()
        )

    async def get_by_id(self, id: UUID) -> Series | None:
        return (
            (
                await self.db.execute(
                    select(Series)
                    .where(Series.id == id)
                    .where(Series.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def create(self, data: CreateSeriesCRUD):
        id = generate_uuid()
        db_series = Series(id, **data.model_dump())
        is_deleted = await self.get_is_deleted(data.name)

        if is_deleted:
            await self.db.execute(
                update(Series).where(Series.name == data.name).values(deleted_at=None)
            )
        if not is_deleted:
            self.db.add(db_series)

        await self.db.commit()

    async def update_by_id(self, id: UUID, series: UpdateSeriesById):
        data = {k: v for k, v in series.model_dump().items() if v is not None}
        data["updated_at"] = datetime.datetime.now()
        await self.db.execute(update(Series).where(Series.id == id).values(data))
        await self.db.commit()

    async def delete_by_id(self, id: UUID):
        await self.db.execute(
            update(Series)
            .where(Series.id == id)
            .values(deleted_at=datetime.datetime.now())
        )
        await self.db.commit()

    async def get_all(self):
        return (
            (
                await self.db.execute(
                    select(Series)
                    .options(
                        defer(Series.created_at),
                        defer(Series.updated_at),
                    )
                    .where(Series.deleted_at.is_(None))
                )
            )
            .scalars()
            .all()
        )

    async def get_is_deleted(self, name: str):
        return (
            (
                await self.db.execute(
                    select(Series)
                    .where(Series.name == name)
                    .where(Series.deleted_at.isnot(None))
                )
            )
            .scalars()
            .first()
        )
