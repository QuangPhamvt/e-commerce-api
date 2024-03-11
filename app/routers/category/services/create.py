from fastapi import HTTPException, status
from app.database.crud import category_crud
from app.schemas.category import CreateCategoryParam
from sqlalchemy.ext.asyncio import AsyncSession


class Create:
    @staticmethod
    async def create(category: CreateCategoryParam, db: AsyncSession):
        is_exist_name = await category_crud.is_exist_name(name=category.name, db=db)
        if is_exist_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name has been used!"
            )
        await category_crud.create_category(category=category, parent_id=None, db=db)
        return {"message": "Create category succeed!"}
