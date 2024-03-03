from app.database import models
from app.schemas.role import CreateRoleParam, Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.utils.uuid import generate_uuid


async def get_role_by_name(db: AsyncSession, role_name: str) -> Role | None:
    # return db.query(models.Role).filter(models.Role.name == role_name).first()
    result = await db.execute(select(models.Role).where(models.Role.name == role_name))
    return result.scalars().first()


async def create_role(db: AsyncSession, role: CreateRoleParam) -> Role:
    role_id = generate_uuid()
    db_role = models.Role(id=role_id, name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role
