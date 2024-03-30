from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.category_crud import CategoryCRUD
from app.schemas.category import CreateCategoryParam, UpdateCategoryParam


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_crud = CategoryCRUD(db)

    async def create(self, category: CreateCategoryParam):
        is_exist_name = await self.category_crud.is_exist(name=category.name)
        if is_exist_name:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")
        await self.category_crud.create(category)
        return {"detail": "Create category succeed!"}

    async def get_all(self):
        list_category = await self.category_crud.read_all()
        return list_category

    async def get_by_id(self, id):
        category = await self.category_crud.read_by_id(id)
        if not category:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found!")
        return category

    async def update(self, id: UUID, category: UpdateCategoryParam):
        is_valid_id = await self.category_crud.read_by_id(id)
        if not is_valid_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id not found!")
        await self.category_crud.update(id, category)
        return {"detail": "Update category succeed!"}

    async def update_product(self, product_id: UUID, category_id: UUID):
        is_valid_id = await self.category_crud.read_by_id(category_id)
        if not is_valid_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id not found!")
        await self.category_crud.update_product(product_id, category_id)
        return {"detail": "Update product category succeed!"}

    async def delete_sub(self, sub_id: UUID, parent_id: UUID):
        is_valid_id = await self.category_crud.read_by_id_and_parent_id(
            sub_id, parent_id
        )
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Incorrect id or parent id!",
            )
        await self.category_crud.delete_sub_by_id(sub_id)
        return {"detail": "Delete category succeed!"}

    async def delete_parent(self, id: UUID):
        is_valid_id = await self.category_crud.read_by_id(id)
        if not is_valid_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id not found!")
        await self.category_crud.delete_parent_by_id(id)
        return {"detail": "Delete category succeed!"}
