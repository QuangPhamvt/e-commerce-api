from app.database.models import Role
from app.schemas.role import CreateRoleParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from app.utils.uuid import generate_uuid
from uuid import UUID


class RoleCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_role_by_name(self, role_name: str) -> Role | None:
        return (
            (await self.db.execute(select(Role).where(Role.name == role_name)))
            .scalars()
            .first()
        )

    async def get_role_id_by_name(self, role_name: str) -> Role | None:
        return (
            (await self.db.execute(select(Role).where(Role.name == role_name)))
            .scalars()
            .first()
        )

    async def get_role_by_id(self, id: UUID) -> Role | None:
        return (
            (await self.db.execute(select(Role).where(Role.id == id))).scalars().first()
        )

    async def create(self, data: CreateRoleParam):
        id = generate_uuid()
        db_role = Role(id, **data.model_dump())
        self.db.add(db_role)
        await self.db.commit()

    async def delete_by_id(self, id: UUID):
        await self.db.execute(delete(Role).where(Role.id == id))
        await self.db.commit()

    async def get_all(self):
        return (await self.db.execute(select(Role))).scalars().all()

    async def update_by_id(self, id: UUID, new_role_name: str):
        await self.db.execute(
            update(Role).where(Role.id == id).values(name=new_role_name)
        )
        await self.db.commit()
