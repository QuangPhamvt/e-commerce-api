from fastapi import APIRouter, Depends, status
from app.services.tag import TagService
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import TAG, TAG_PATH, TAG_PREFIX
from app.dependencies import get_db

CREATE_TAG = TAG_PATH["CREATE_TAG"]
GET_LIST_TAG = TAG_PATH["GET_LIST_TAG"]
DELETE_TAG = TAG_PATH["DELETE_TAG"]
router = APIRouter(prefix=TAG_PREFIX, tags=[TAG])


@router.get(
    GET_LIST_TAG,
    description="This endpoint is used to get list of tags.",
    status_code=status.HTTP_200_OK,
    responses={200: {"detail": "Get List Tags Succeed!"}},
)
async def get_list_tags(db: AsyncSession = Depends(get_db)):
    return await TagService().get_all(db)
