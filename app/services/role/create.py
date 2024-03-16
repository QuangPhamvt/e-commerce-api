from fastapi import HTTPException, status
from app.database.crud import role_crud
from app.schemas.role import CreateRoleParam
from sqlalchemy.ext.asyncio import AsyncSession


class Create:
    @staticmethod
    async def create(*, role: CreateRoleParam, db: AsyncSession):
        is_exist_name = await role_crud.get_role_by_name(db=db, role_name=role.name)
        if is_exist_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name has been used!",
            )
        await role_crud.create_role(db=db, role=role)
        return {"detail": "Create role succeed!"}
