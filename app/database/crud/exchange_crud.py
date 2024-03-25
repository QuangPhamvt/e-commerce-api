from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update

from app.database.models import ExchangeRate
from app.schemas.exchange import CreateExchangeData, UpdateExchangeData
from app.utils.uuid import generate_uuid


async def is_exist_currency(currency: str, db: AsyncSession) -> UUID | None:
    exchange = await db.execute(
        select(ExchangeRate.id).where(ExchangeRate.currency == currency)
    )
    return exchange.scalars().first()


async def get_exchange_rate_by_id(id: UUID, db: AsyncSession) -> ExchangeRate | None:
    deposit = await db.execute(select(ExchangeRate).where(ExchangeRate.id == id))
    return deposit.scalars().first()


async def create_exchange_rate(data: CreateExchangeData, db: AsyncSession):
    id = generate_uuid()
    exchange_rate = ExchangeRate(id, **data.model_dump())
    db.add(exchange_rate)
    await db.commit()


async def update_exchange_rate(id: UUID, data: UpdateExchangeData, db: AsyncSession):
    await db.execute(
        update(ExchangeRate).where(ExchangeRate.id == id).values(**data.model_dump())
    )
    await db.commit()


async def get_list_exchange(db: AsyncSession):
    deposit = await db.execute(select(ExchangeRate))
    return deposit.scalars().all()


async def delete_exchange_rate_by_id(id: UUID, db: AsyncSession):
    await db.execute(delete(ExchangeRate).where(ExchangeRate.id == id))
    await db.commit()
