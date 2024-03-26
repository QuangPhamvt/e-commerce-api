from datetime import datetime
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.database.models.Product import DepositType
from app.schemas.deposit import CreateDepositData, UpdateDepositData
from app.utils.uuid import generate_uuid


async def is_exist_name(name: str, db: AsyncSession) -> UUID | None:
    deposit = await db.execute(select(DepositType.id).where(DepositType.name == name))
    return deposit.scalars().first()


async def create_deposit_type(data: CreateDepositData, db: AsyncSession):
    id = generate_uuid()
    deposit_type = DepositType(id, **data.model_dump())
    db.add(deposit_type)
    await db.commit()


async def get_deposit_type_by_id(id: UUID, db: AsyncSession) -> DepositType | None:
    deposit = await db.execute(select(DepositType).where(DepositType.id == id))
    return deposit.scalars().first()


async def update_deposit_type(id: UUID, data: UpdateDepositData, db: AsyncSession):
    await db.execute(
        update(DepositType)
        .where(DepositType.id == id)
        .values(**data.model_dump(), updated_at=datetime.today())
    )
    await db.commit()


async def get_list_deposit(db: AsyncSession):
    deposit = await db.execute(select(DepositType))
    return deposit.scalars().all()


async def delete_deposit_type_by_id(id: UUID, db: AsyncSession):
    await db.execute(delete(DepositType).where(DepositType.id == id))
    await db.commit()
