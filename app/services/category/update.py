from fastapi import HTTPException, status
from app.database.crud import category_crud
from app.schemas.category import UpdateCategoryParam
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.uuid import convert_str_to_uuid


class Update:
    @staticmethod
    async def update(id: str, category: UpdateCategoryParam, db: AsyncSession):
        category_id = convert_str_to_uuid(id)
        is_valid_id = await category_crud.get_category_by_id(id=category_id, db=db)
        if not is_valid_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id not found!")
        await category_crud.update_category(id=category_id, category=category, db=db)
        return {"detail": "Update category succeed!"}
