from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud.category_crud import CategoryCRUD
from app.schemas.category import (
    CreateCategoryParam,
    UpdateCategoryData,
    UpdateCategoryParam,
)


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_crud = CategoryCRUD(db)

    async def create(self, category: CreateCategoryParam):
        is_exist_name = await self.category_crud.is_exist(name=category.name)
        if is_exist_name:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")
        if category.parent_id:
            is_valid_parent_id = await self.category_crud.read_by_id(category.parent_id)
            if not is_valid_parent_id:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Parent id not found!")
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
        if (category.sub_id is not None) and (category.parent_id is not None):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "parent_id and sub_id cannot be used at the same time!",
            )
        is_valid_id = await self.category_crud.read_by_id(id)
        if not is_valid_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id not found!")
        list_invalid_id = []
        list_valid_id: list[UUID] = []
        if category.sub_id:
            list_sub_id = category.sub_id
            list_category = await self.category_crud.read_list_id()
            for sub_id in list_sub_id:
                if sub_id not in list_category:
                    list_invalid_id.append(sub_id)
                else:
                    list_valid_id.append(sub_id)
            await self.category_crud.update_parent_id_for_subcategory(id, list_valid_id)
        data_update = UpdateCategoryData(**category.model_dump())
        await self.category_crud.update(id, data_update)
        list_invalid_id = [str(id) for id in list_invalid_id]
        message_append = f"Can not update {list_invalid_id} because id not found!"
        return {
            "detail": f"Update category succeed! {message_append if len(list_invalid_id) > 0 else ''}"
        }

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
