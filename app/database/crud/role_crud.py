from app.database.models import Role
from app.schemas.role import CreateRoleParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.utils.uuid import generate_uuid
from uuid import UUID


async def get_role_by_name(db: AsyncSession, role_name: str) -> Role | None:
    # return db.query(models.Role).filter(models.Role.name == role_name).first()
    result = await db.execute(select(Role).where(Role.name == role_name))
    return result.scalars().first()


async def get_role_id_by_name(db: AsyncSession, role_name: str) -> UUID | None:
    result = await db.execute(select(Role.id).where(Role.name == role_name))
    return result.scalars().first()

async def get_role_by_id(id: UUID, db: AsyncSession) -> UUID | None:
    role = await db.execute(select(Role).where(Role.id == id))
    return role.scalars().first()

async def create_role(db: AsyncSession, role: CreateRoleParam) -> Role:
    role_id = generate_uuid()
    db_role = Role(role_id, name=role.name)
    db.add(db_role)
    await db.commit()
    await db.refresh(db_role)
    return db_role

async def get_list_role(db: AsyncSession):
    list_roles = await db.execute(select(Role))
    return list_roles.scalars().all()

async def delete_role_by_id(role_id: UUID, db: AsyncSession):
    await db.execute(delete(Role).where(Role.id == role_id))
    await db.commit()

async def update_role_by_id(role_id: UUID, new_role_name: str, db: AsyncSession):
    await db.execute(
        update(Role).where(Role.id == role_id).values(name=new_role_name)
    )
    await db.commit()