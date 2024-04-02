from uuid import UUID
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tag import CreateTagData, CreateTagParam, TagBase
from app.database.crud.tag_crud import TagCRUD
from app.database.crud.product_tag_crud import ProductTagCRUD


class TagService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tag_crud = TagCRUD(db)
        self.product_tag_crud = ProductTagCRUD(db)

    async def create(self, body: CreateTagParam):
        is_exist = await self.__is_exist_tag(body.name)
        if is_exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")

        data = CreateTagData(**body.model_dump())
        await self.tag_crud.create(data)

        return {"detail": "Create Tag Succeed!"}

    async def create_bulk(self, tags: list[TagBase]):
        list_tag_name = await self.tag_crud.read_all_name()
        list_tag_name = list(map(lambda x: x.lower(), list_tag_name))
        for tag in tags:
            if tag.name.lower() in list_tag_name:
                continue
            await self.tag_crud.create(tag)
        return {"detail": "Create List Tag Succeed!"}

    async def get_all(self):
        tags = await self.tag_crud.read_all()
        return tags

    async def delete(self, id: UUID):
        is_exist = await self.tag_crud.read_by_id(id)
        if not is_exist:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Tag Not Found!")

        await self.tag_crud.delete(id)
        return {"detail": "Delete Tag Succeed!"}

    async def add_product_tag(self, id: UUID, tags: list[TagBase]):
        for tag in tags:
            name = tag.name
            tag_id = await self.tag_crud.is_exist_name(name)
            if not tag_id:
                await self.tag_crud.create(tag)
            tag_id = await self.tag_crud.is_exist_name(name)
            if tag_id:
                is_relation_exist = await self.product_tag_crud.is_exist(id, tag_id)
                if not is_relation_exist:
                    await self.product_tag_crud.create(id, tag_id)

        return {"detail": "Tags Already For Product Exist!"}

    async def __is_exist_tag(self, name: str):
        is_exist = await self.tag_crud.is_exist_name(name)
        return is_exist
