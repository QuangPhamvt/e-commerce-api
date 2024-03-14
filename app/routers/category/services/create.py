from fastapi import HTTPException, status
from app.database.crud import category_crud
from app.schemas.category import CreateCategoryParam
from sqlalchemy.ext.asyncio import AsyncSession


class Create:
    @staticmethod
    async def create(category: CreateCategoryParam, db: AsyncSession):
        is_exist_name = await category_crud.is_exist_name(name=category.name, db=db)
        if is_exist_name:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")
        await category_crud.create_category(category, None, db)
        return {"detail": "Create category succeed!"}
