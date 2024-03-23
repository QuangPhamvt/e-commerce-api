from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.database.crud import tag_crud, product_tag_crud


class GetProductsByTag:
    async def get_products_by_tag(self, tag_name: str, db: AsyncSession):
        tag_id = await self.__get_tag_id(tag_name, db)
        products = await product_tag_crud.get_list_products_by_tag(tag_id, db)
        return products

    @staticmethod
    async def __get_tag_id(tag_name: str, db: AsyncSession):
        tag_id = await tag_crud.is_exist_name(tag_name, db)
        if not tag_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tag not found!")
        return tag_id
