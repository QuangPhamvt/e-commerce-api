from fastapi import HTTPException, status
from app.configs.S3.delete_object import delete_object_s3
from app.database.crud import series_crud
from app.utils.uuid import convert_str_to_uuid
from sqlalchemy.ext.asyncio import AsyncSession


class Delete:
    async def delete(self, id: str, db: AsyncSession):
        series_id = convert_str_to_uuid(id)
        series = await series_crud.get_series_by_id(id=series_id, db=db)
        if not series:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Series not found!"
            )
        await self.__delete_image_S3(series.image)
        await series_crud.delete_series(id=series_id, db=db)
        return {"detail": "Delete Series Succeed!"}

    @staticmethod
    async def __delete_image_S3(image: str):
        delete_object_s3("customafk-ecommerce-web", image)
        pass
