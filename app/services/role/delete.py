from fastapi import HTTPException, status
from app.database.crud import role_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper


class Delete:
    @staticmethod
    async def delete(id: str, db: AsyncSession):
        role_id = helper.convert_str_to_UUID(id)
        is_valid_id = await role_crud.get_role_by_id(role_id, db)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        await role_crud.delete_role_by_id(role_id, db)
        return {"detail": "Delete Role succeed!"}
