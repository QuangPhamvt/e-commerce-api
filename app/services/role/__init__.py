from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.role_crud import RoleCRUD

from app.schemas.role import CreateRoleParam


class RoleService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.role_crud = RoleCRUD(db)

    async def create(self, role: CreateRoleParam):
        is_exist_name = await self.role_crud.get_role_by_name(role.name)
        if is_exist_name:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Name has been used!",
            )
        await self.role_crud.create(role)
        return {"detail": "Create role succeed!"}

    async def get_all(self):
        return await self.role_crud.get_all()

    async def update(self, id: UUID, new_role_name: str):
        is_valid_id = await self.role_crud.get_role_by_id(id)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )

        await self.role_crud.update_by_id(
            id,
            new_role_name,
        )
        return {"detail": "Update role succeed!"}

    async def delete(self, id: UUID):
        is_valid_id = await self.role_crud.get_role_by_id(id)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        await self.role_crud.delete_by_id(id)
        return {"detail": "Delete Role succeed!"}
