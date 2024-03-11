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
        print(f"parentId: {parent_id}, id: {id}")
        if not is_valid_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect id or parent id!",
            )

        await category_crud.delete_category(id=id, db=db)
        return {"message": "Delete category succeed!"}
