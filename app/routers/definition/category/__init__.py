from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import CATEGORY, CATEGORY_PREFIX
from app.dependencies import get_db
from app.services.category import CategoryService


router = APIRouter(prefix=CATEGORY_PREFIX, tags=[CATEGORY])


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
