from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import CATEGORY, CATEGORY_PREFIX
from app.dependencies import get_db
from app.schemas.category import CreateCategoryParam, UpdateCategoryParam
from app.schemas.responses import Res201Resquest
from app.services.category import CategoryService


router = APIRouter(prefix=CATEGORY_PREFIX, tags=[CATEGORY])


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
    return await CategoryService().create(category, db)


# ********** SUB-CATEGORY **********
@router.post(
    "/{id}",
    description="This endpoint is used to create a sub-category",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Create sub-category succeed!", "model": Res201Resquest}
    },
)
async def create_sub_category(
    category: CreateCategoryParam, id: str, db: AsyncSession = Depends(get_db)
):
    return await CategoryService().create_sub(category, id, db)


@router.delete(
    "/{id}",
    description="This endpoint is used to delete a category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete category succeed!"}},
)
async def delete_category(id: str, db: AsyncSession = Depends(get_db)):
    return await CategoryService().delete(id=id, db=db)


@router.delete(
    "/{parent_id}/sub-categories/{id}",
    description="This endpoint is used to delete a sub-category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete category succeed!"}},
)
async def delete_sub_category(
    id: str, parent_id: str, db: AsyncSession = Depends(get_db)
):
    return await CategoryService().delete_sub(raw_id=id, raw_parent_id=parent_id, db=db)


@router.put(
    "/{id}",
    description="This endpoint is used to update a category",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete category succeed!"}},
)
async def update_category(
    id: str, category: UpdateCategoryParam, db: AsyncSession = Depends(get_db)
):
    return await CategoryService().update(id=id, category=category, db=db)


@router.get(
    "/",
    description="This endpoint is used to get list of category",
    status_code=status.HTTP_200_OK,
    responses={200: {"Description": "Get list category succeed!"}},
)
async def get_categories(
    current: Annotated[str | None, Query()] = None,
    limit: Annotated[str | None, Query()] = None,
    db: AsyncSession = Depends(get_db),
):
    current_page = int(current) if current else 1
    default_limit = int(limit) if limit else 10
    return await CategoryService().get_all(
        current=current_page, limit=default_limit, db=db
    )
