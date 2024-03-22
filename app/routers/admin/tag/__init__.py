from fastapi import APIRouter, Depends, status
from app.services.tag import TagService
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import TAG, TAG_PATH, TAG_PREFIX
from app.dependencies import get_db
from app.schemas.tag import CreateTagParam, TagBase


CREATE_TAG = TAG_PATH["CREATE_TAG"]
GET_LIST_TAG = TAG_PATH["GET_LIST_TAG"]
DELETE_TAG = TAG_PATH["DELETE_TAG"]
ADD_PRODUCT_TAGS = TAG_PATH["ADD_PRODUCT_TAGS"]

router = APIRouter(prefix=TAG_PREFIX, tags=[TAG])


# ********** CREATE TAG **********
@router.post(
    CREATE_TAG,
    description="This endpoint is used to create a new tag.",
    status_code=status.HTTP_201_CREATED,
    responses={201: {"detail": "Create tag succeed!"}},
)
async def create_product(body: CreateTagParam, db: AsyncSession = Depends(get_db)):
    return await TagService().create(body, db)


@router.get(
    GET_LIST_TAG,
    description="This endpoint is used to get list of tags.",
    status_code=200,
    responses={200: {"detail": "Get List Tags Succeed!"}},
)
async def get_list_tags(db: AsyncSession = Depends(get_db)):
    return await TagService().get_all(db)


@router.delete(
    DELETE_TAG,
    response_description="This endpoint is used to delete a tag by id.",
    status_code=200,
    responses={200: {"detail": "Delete Tag Succeed!"}},
)
async def delete_product(id: str, db: AsyncSession = Depends(get_db)):
    return await TagService().delete(id=id, db=db)


@router.post(
    ADD_PRODUCT_TAGS,
    description="This endpoint is used to add tags for a product. If tag is not exist, it will be created and added for the product.",
    status_code=200,
    responses={200: {"detail": "Add Tags For Product Succeed!"}},
)
async def add_product_tags(
    product_id: str, tags: list[TagBase], db: AsyncSession = Depends(get_db)
):
    return await TagService().add(product_id, tags, db)
