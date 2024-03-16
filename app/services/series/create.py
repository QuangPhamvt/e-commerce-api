from fastapi import HTTPException, status
from app.configs.S3.put_object import put_object
from app.database.crud import series_crud
from app.schemas.series import CreateSeriesData, CreateSeriesParam
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.helper import helper


class Create:
    async def create(self, body: CreateSeriesParam, db: AsyncSession):
        is_exist = await self.__is_exist_series(name=body.name, db=db)
        if is_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name has been used!"
            )
        slug = helper.slugify(body.name)
        image = f"series/{slug}.webp"
        data = CreateSeriesData(slug=slug, image=image, **body.model_dump())
        await series_crud.create(data=data, db=db)
        new_series = self.__create_presigned_url("customafk-ecommerce-web", slug)

        if new_series is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
            )

        return {"detail": "Create Series Succeed!", "presigned_url": new_series}

    @staticmethod
    async def __is_exist_series(name: str, db: AsyncSession):
        is_exist = await series_crud.get_series_by_name(name=name, db=db)
        return is_exist

    @staticmethod
    def __create_presigned_url(bucket_name: str, slug: str):
        url = f"series/{slug}.webp"
        return put_object(bucket_name, url)
