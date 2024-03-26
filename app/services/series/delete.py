from fastapi import HTTPException, status
from app.configs.S3.delete_object import delete_object_s3
from app.database.crud import series_crud
from app.utils.uuid import convert_str_to_uuid
from sqlalchemy.ext.asyncio import AsyncSession


class Delete:
    async def delete(self, id: str, db: AsyncSession):
        series_id = convert_str_to_uuid(id)
        series = await series_crud.get_series_by_id(series_id, db)
        if not series:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")
        self.__delete_image_S3(series.image)
        await series_crud.delete_series(series_id, db)
        return {"detail": "Delete Series Succeed!"}

    @staticmethod
    def __delete_image_S3(image: str):
        delete_object_s3("customafk-ecommerce-web", image)
        pass
