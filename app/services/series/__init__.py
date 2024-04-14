import logging
from typing import Sequence
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.Clounfront import get_image_from_url
from app.configs.S3.delete_object import delete_object_s3
from app.configs.S3.put_object import put_object
from app.configs.constants import BUCKET_NAME
from app.database.crud.series_crud import SeriesCRUD
from app.database.models.Product import Series

from app.schemas.series import (
    CreateSeriesBody,
    CreateSeriesCRUD,
    UpdateSeriesById,
    UpdateSeriesParam,
)
from app.utils.helper import helper
from app.utils.uuid import convert_str_to_uuid


class SeriesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.series_crud = SeriesCRUD(db)
        if BUCKET_NAME is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Bucket name is not set!")
        self.BUCKET_NAME = BUCKET_NAME

    async def create(self, body: CreateSeriesBody):
        name = body.name
        image_type = body.image_type

        slug = helper.slugify(name)
        image = f"series/{slug}.{image_type}"

        is_exist = await self.__is_exist_series(body.name)
        logging.warn(f"{is_exist}")
        if is_exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")

        data = CreateSeriesCRUD(slug=slug, image=image, **body.model_dump())
        await self.series_crud.create(data)

        new_series = self.__create_presigned_url(self.BUCKET_NAME, slug, image_type)

        if new_series is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
            )

        return {"detail": "Create Series Succeed!", "presigned_url": new_series}

    async def get_all(self):
        try:
            series = await self.series_crud.get_all()
            new_series = self.__convert_image_to_url(series)
            return new_series
        except Exception as e:
            logging.warn(f"{e}")
            return {"detail": "Failed to get all series"}

    async def update(self, id: UUID, body: UpdateSeriesParam):
        slug = helper.slugify(body.name)

        is_valid = await self.series_crud.get_by_id(id)
        if not is_valid:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")

        is_exist = await self.__is_exist_series(body.name)
        if is_exist:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Name has been used!")

        try:
            data = UpdateSeriesById(slug=slug, **body.model_dump())
            await self.series_crud.update_by_id(id, data)
            return {"detail": f"Update Series {id} Succeed!"}
        except Exception as e:
            logging.warn(f"{e}")
            return {"detail": f"Failed to update series {id}"}

    async def delete(self, id: str):
        series_id = convert_str_to_uuid(id)
        series = await self.series_crud.get_by_id(series_id)

        if not series:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")
        self.__delete_image_S3(series.image)
        await self.series_crud.delete_by_id(series_id)
        return {"detail": "Delete Series Succeed!"}

    async def __is_exist_series(self, name: str):
        is_exist = await self.series_crud.is_exist_name(name)
        return is_exist

    @staticmethod
    def __create_presigned_url(bucket_name: str, slug: str, image_type: str):
        url = f"series/{slug}.{image_type}"
        type = f"image/{image_type}"
        return put_object(bucket_name, url, type)

    @staticmethod
    def __convert_image_to_url(series: Sequence[Series]) -> Sequence[Series]:
        data = [
            Series(
                item.id,
                item.name,
                item.slug,
                item.description,
                get_image_from_url(item.image),
            )
            for item in series
        ]

        return data

    def __delete_image_S3(self, image: str):
        delete_object_s3(self.BUCKET_NAME, image)
        pass
