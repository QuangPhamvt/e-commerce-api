from app.database import models
from app.schemas.role import CreateRoleParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.uuid import generate_uuid
from uuid import UUID


async def get_role_by_name(db: AsyncSession, role_name: str) -> models.Role | None:
    # return db.query(models.Role).filter(models.Role.name == role_name).first()
    result = await db.execute(select(models.Role).where(models.Role.name == role_name))
    return result.scalars().first()


async def get_role_id_by_name(db: AsyncSession, role_name: str) -> UUID | None:
    result = await db.execute(
        select(models.Role.id).where(models.Role.name == role_name)
    )
    return result.scalars().first()


async def create_role(db: AsyncSession, role: CreateRoleParam) -> models.Role:
    role_id = generate_uuid()
    db_role = models.Role(role_id, name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role
