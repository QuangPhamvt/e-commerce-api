from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import series_crud
from app.database.models.Product import Series
from app.configs.Clounfront import get_image_from_url


class GetAll:
    async def get_all(self, db: AsyncSession):
        series = await series_crud.get_all(db)
        new_series = self.__convert_image_to_url(series)
        return new_series

    @staticmethod
    def __convert_image_to_url(series: Sequence[Series]) -> Sequence[Series]:
        for item in series:
            DOMAIN_IMAGE = get_image_from_url(item.image)
            if DOMAIN_IMAGE:
                item.image = DOMAIN_IMAGE
        return series
