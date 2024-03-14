from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import category_crud

from app.utils.uuid import convert_str_to_uuid


class Delete:
    @staticmethod
    async def delete(id: str, db: AsyncSession):
        category_id = convert_str_to_uuid(id)
        is_valid_id = await category_crud.get_category_by_id(category_id, db)
        if not is_valid_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id not found!")
        await category_crud.delete_sub_category_by_parent_id(category_id, db)
        await category_crud.delete_category(category_id, db)
        return {"detail": "Delete category succeed!"}
