from fastapi import HTTPException, status
from app.database.crud import role_crud
from app.schemas.role import CreateRoleParam
from app.database.models import Role
from sqlalchemy.ext.asyncio import AsyncSession


class RoleService:
    @staticmethod
    async def create(*, role: CreateRoleParam, db: AsyncSession) -> Role:
        db_role = await role_crud.get_role_by_name(db=db, role_name=role.name)
        if db_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name has been used!"
            )
        new_role = await role_crud.create_role(db=db, role=role)
        return new_role


role_service: RoleService = RoleService()
