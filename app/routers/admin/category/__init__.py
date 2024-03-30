from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import CATEGORY, CATEGORY_PREFIX
from app.dependencies import get_db
from app.schemas.category import (
    CreateCategoryParam,
    UpdateCategoryParam,
    UpdateProductCategoryParam,
)
from app.schemas.responses import Res201Resquest
from app.services.category import CategoryService


router = APIRouter(prefix=CATEGORY_PREFIX, tags=[CATEGORY])


# ********** CATEGORY **********
@router.get(
    "",
    description="This endpoint is used to get list of category",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Get list category succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "51babb32-40f4-4d14-bff2-4c035d09fcd0",
                            "name": "Category 1",
                            "slug": "category-1",
                            "description": "Category 1 description",
                            "sub": [],
                        }
                    ]
                }
            },
        }
    },
)
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryService(db).get_all()


# ********** CATEGORY **********
@router.post(
    "",
    description="This endpoint is used to create a category",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Create category succeed!", "model": Res201Resquest}
    },
)
async def create_category(
    category: CreateCategoryParam, db: AsyncSession = Depends(get_db)
):
    return await CategoryService(db).create(category)


@router.put(
    "/products",
    description="This endpoint is used to update a product category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Update product category succeed!"}},
)
async def update_product_category(
    body: UpdateProductCategoryParam, db: AsyncSession = Depends(get_db)
):
    return await CategoryService(db).update_product(body.product_id, body.category_id)


@router.put(
    "/{id}",
    description="This endpoint is used to update a category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete category succeed!"}},
)
async def update_category(
    id: UUID, category: UpdateCategoryParam, db: AsyncSession = Depends(get_db)
):
    return await CategoryService(db).update(id, category)


@router.delete(
    "/{id}",
    description="This endpoint is used to delete a category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete category succeed!"}},
)
async def delete_category(id: UUID, db: AsyncSession = Depends(get_db)):
    return await CategoryService(db).delete_parent(id)


@router.delete(
    "/{parent_id}/sub-categories/{id}",
    description="This endpoint is used to delete a sub-category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete category succeed!"}},
)
async def delete_sub_category(
    id: UUID, parent_id: UUID, db: AsyncSession = Depends(get_db)
):
    return await CategoryService(db).delete_sub(id, parent_id)
