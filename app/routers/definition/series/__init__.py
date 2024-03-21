from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import SERIES, SERIES_PREFIX, SERIES_PATH
from app.dependencies import get_db
from app.services.series import SeriesService
from app.schemas.series import ListSeriesResponse

GET_LIST_SERIES = SERIES_PATH["GET_LIST_SERIES"]

router = APIRouter(prefix=SERIES_PREFIX, tags=[SERIES])


@router.get(
    GET_LIST_SERIES,
    description="This endpoint is used to get list of series.",
    status_code=status.HTTP_200_OK,
    response_model=list[ListSeriesResponse],
    responses={
        "200": {
            "description": "Get List Series Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Naruto",
                            "description": "A young ninja's quest to become the strongest leader.",
                            "image": "http://example.com/naruto.jpg",
                            "slug": "naruto",
                            "id": "123e4567e89b12d3a456426614174001",
                        },
                        {
                            "name": "Harry Potter",
                            "description": "A young wizard's adventures at Hogwarts School.",
                            "image": "http://example.com/harry_potter.jpg",
                            "slug": "harry-potter",
                            "id": "123e4567e89b12d3a456426614174002",
                        },
                    ]
                },
            },
        },
    },
)
async def get_list_series(db: AsyncSession = Depends(get_db)):
    return await SeriesService().get_all(db)
