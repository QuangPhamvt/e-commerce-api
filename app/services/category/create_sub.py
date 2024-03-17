from fastapi import HTTPException, status
from app.database.crud import category_crud
from app.schemas.category import CreateCategoryParam
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.uuid import convert_str_to_uuid


class CreateSub:
    @staticmethod
    async def create_sub(category: CreateCategoryParam, id: str, db: AsyncSession):
        is_exist_name = await category_crud.is_exist_name(name=category.name, db=db)
        if is_exist_name:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")
        parent_id = convert_str_to_uuid(id)
        is_valid_parent_id = await category_crud.get_category_by_id(parent_id, db)
        if not is_valid_parent_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Parent's id not found!")
        await category_crud.create_category(category, parent_id, db)
        return {"detail": "Create Sub-category Succeed!"}
