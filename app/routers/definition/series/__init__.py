from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import SERIES, SERIES_PREFIX
from app.dependencies import get_db
from app.services.series import SeriesService


router = APIRouter(prefix=SERIES_PREFIX, tags=[SERIES])


@router.get(
    "/",
    description="This endpoint is used to get list of series.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Series Succeed!",
        },
    },
)
async def get_list_products(db: AsyncSession = Depends(get_db)):
    return await SeriesService().get_all(db)
