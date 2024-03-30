from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import SERIES, SERIES_PREFIX
from app.dependencies import get_db
from app.schemas.responses import Res201Resquest
from app.schemas.series import (
    CreateSeriesBody,
    CreateSeriesResponse,
    UpdateSeriesParam,
)
from app.services.series import SeriesService


router = APIRouter(prefix=SERIES_PREFIX, tags=[SERIES])


# ********** GET LIST SERIES **********
@router.get(
    "",
    description="This endpoint is used to get list of series.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Series Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Series 1",
                            "id": "67b5ab15-ee53-446e-8fe5-7ab13bac7ff7",
                            "description": "Series 1 description",
                            "slug": "series-1",
                            "image": "https://customafk-ecommerce-web.s3.amazonaws.com/series/series-1.webp",
                        }
                    ]
                }
            },
        },
    },
)
async def get_list_products(db: AsyncSession = Depends(get_db)):
    return await SeriesService(db).get_all()


# ********** CREATE SERIES **********
@router.post(
    "",
    description="This endpoint is used to create a new series.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": CreateSeriesResponse},
    },
)
async def create_product(body: CreateSeriesBody, db: AsyncSession = Depends(get_db)):
    return await SeriesService(db).create(body)


@router.put(
    "/{id}",
    description="This endpoint is used to update a series by id.",
    status_code=200,
    responses={
        200: {"description": "Update Series Succeed!", "model": Res201Resquest},
    },
)
async def update_product(
    id: UUID, body: UpdateSeriesParam, db: AsyncSession = Depends(get_db)
):
    return await SeriesService(db).update(id, body)


@router.delete(
    "/{id}",
    response_description="This endpoint is used to delete a series by id.",
    status_code=200,
    responses={
        200: {"description": "Delete Series Succeed!", "model": Res201Resquest},
    },
)
async def delete_product(id: str, db: AsyncSession = Depends(get_db)):
    return await SeriesService(db).delete(id)
