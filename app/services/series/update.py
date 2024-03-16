from fastapi import HTTPException, status
from app.database.crud import series_crud
from app.schemas.series import UpdateSeriesData, UpdateSeriesParam
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.helper import helper
from app.utils.uuid import convert_str_to_uuid


class Update:
    @staticmethod
    async def update(id: str, body: UpdateSeriesParam, db: AsyncSession):
        series_id = convert_str_to_uuid(raw_id=id)
        is_valid = await series_crud.get_series_by_id(id=series_id, db=db)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Series not found!"
            )
        slug = helper.slugify(body.name)
        data = UpdateSeriesData(slug=slug, **body.model_dump())
        await series_crud.update_series(id=series_id, data=data, db=db)
        return {"detail": f"Update Series {series_id} Succeed!"}
