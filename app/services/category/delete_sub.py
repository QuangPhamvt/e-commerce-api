from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import category_crud

from app.utils.uuid import convert_str_to_uuid


class DeleteSub:
    @staticmethod
    async def delete_sub(raw_id: str, raw_parent_id: str, db: AsyncSession):
        parent_id = convert_str_to_uuid(raw_parent_id)
        id = convert_str_to_uuid(raw_id)
        is_valid_id = await category_crud.get_category_by_id_and_parent_id(
            id=id, parent_id=parent_id, db=db
        )
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Incorrect id or parent id!",
            )

        await category_crud.delete_category(id=id, db=db)
        return {"detail": "Delete category succeed!"}
