from fastapi import APIRouter, Depends, status
from app.services.tag import TagService
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import TAG, TAG_PATH, TAG_PREFIX
from app.dependencies import get_db
from app.schemas.tag import ListTagRespone

CREATE_TAG = TAG_PATH["CREATE_TAG"]
GET_LIST_TAG = TAG_PATH["GET_LIST_TAG"]
DELETE_TAG = TAG_PATH["DELETE_TAG"]
router = APIRouter(prefix=TAG_PREFIX, tags=[TAG])


@router.get(
    GET_LIST_TAG,
    description="This endpoint is used to get list of tags.",
    status_code=status.HTTP_200_OK,
    response_model=list[ListTagRespone],
    responses={
        "200": {
            "description": "Get List Tags Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Yêu Thích",
                            "id": "123e4567e89b12d3a456426614174006",
                        },
                        {
                            "name": "Pre-order",
                            "id": "123e4567e89b12d3a456426614174007",
                        },
                    ]
                },
            },
        },
    },
)
async def get_list_tags(db: AsyncSession = Depends(get_db)):
    return await TagService().get_all(db)
