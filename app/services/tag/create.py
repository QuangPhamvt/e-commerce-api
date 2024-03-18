from fastapi import HTTPException, status
from app.schemas.tag import CreateTagData, CreateTagParam
from app.database.crud import tag_crud
from sqlalchemy.ext.asyncio import AsyncSession


class Create:
    async def create(self, body: CreateTagParam, db: AsyncSession):
        is_exist = await self.__is_exist_tag(body.name, db)
        if is_exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")
        data = CreateTagData(**body.model_dump())
        await tag_crud.create(data=data, db=db)

        return {"detail": "Create Tag Succeed!"}

    @staticmethod
    async def __is_exist_tag(name: str, db: AsyncSession):
        is_exist = await tag_crud.is_exist_name(name, db)
        return is_exist
