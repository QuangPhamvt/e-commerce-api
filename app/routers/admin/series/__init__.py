from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import SERIES, SERIES_PREFIX
from app.dependencies import get_db
from app.schemas.responses import Res201Resquest
from app.schemas.series import (
    CreateSeriesParam,
    CreateSeriesResponse,
    UpdateSeriesParam,
)
from app.services.series import SeriesService


router = APIRouter(prefix=SERIES_PREFIX, tags=[SERIES])


# ********** CREATE SERIES **********
@router.post(
    "",
    description="This endpoint is used to create a new series.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": CreateSeriesResponse},
    },
)
async def create_product(body: CreateSeriesParam, db: AsyncSession = Depends(get_db)):
    return await SeriesService().create(body, db)


@router.put(
    "/{id}",
    description="This endpoint is used to update a series by id.",
    status_code=200,
    responses={
        200: {"description": "Update Series Succeed!", "model": Res201Resquest},
    },
)
async def update_product(
    id: str, body: UpdateSeriesParam, db: AsyncSession = Depends(get_db)
):
    return await SeriesService().update(id, body, db)


@router.delete(
    "/{id}",
    response_description="This endpoint is used to delete a series by id.",
    status_code=200,
    responses={
        200: {"description": "Delete Series Succeed!", "model": Res201Resquest},
    },
)
async def delete_product(id: str, db: AsyncSession = Depends(get_db)):
    return await SeriesService().delete(id=id, db=db)


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
