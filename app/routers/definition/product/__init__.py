import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import PRODUCT, PRODUCT_PREFIX
from app.dependencies import get_db
from app.schemas.responses import ResBadRequest
from app.services.product import ProductService

router = APIRouter(
    prefix=PRODUCT_PREFIX,
    tags=[PRODUCT],
)


# ********** GET LIST PRODUCTS **********
@router.get(
    "",
    description="This endpoint is used to get list of products.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Products Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "92792ee8-011b-4f9a-be7d-9f1c29eea149",
                            "country": "USA",
                            "series_id": "string",
                            "thumbnail": "https://dev.image.customafk.com/products/iphone-13.jpeg",
                            "factory": "Apple",
                            "variant": "string",
                            "name": "Iphone 13asdasd",
                            "status": "IN STOCK",
                            "preorder_start_date": "string",
                            "original_price": 1000,
                            "category_id": "6f4ffeb0-750f-49d3-ab4c-c2c8d8c4b343",
                            "preorder_end_date": "string",
                            "sell_price": 900,
                            "quantity": 100,
                            "description": "This is a new product from Apple",
                            "slug": "iphone-13asdasd",
                        }
                    ]
                }
            },
        },
    },
)
async def get_list_products(db: AsyncSession = Depends(get_db)):
    try:
        data = await ProductService(db).get_all()
        new_data = []
        for item in data:
            item.__dict__.pop("original_price") if item.__dict__.get(
                "original_price"
            ) else None
            new_data.append(item)
        return new_data
    except Exception as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, f"Get List Products Failed! {e}"
        )


# ********** GET PRODUCT BY ID **********
@router.get(
    "/{id}",
    description="This endpoint is used to get a product by id.",
    status_code=200,
    responses={
        400: {"model": ResBadRequest, "description": "Not Found"},
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "tags": [],
                        "category": {
                            "slug": "category-1",
                            "parent_id": None,
                            "description": "Category 1 description",
                            "id": "6f4ffeb0-750f-49d3-ab4c-c2c8d8c4b343",
                            "name": "Category 1",
                        },
                        "country": "USA",
                        "thumbnail": "https://dev.image.customafk.com/products/iphone-13.jpeg",
                        "factory": "Apple",
                        "variant": None,
                        "name": "Iphone 13asdasd",
                        "status": "IN STOCK",
                        "preorder_start_date": None,
                        "preorder_end_date": None,
                        "sell_price": 900,
                        "quantity": 100,
                        "description": "This is a new product from Apple",
                        "slug": "iphone-13asdasd",
                        "id": "92792ee8-011b-4f9a-be7d-9f1c29eea149",
                    }
                }
            }
        },
    },
)
async def get_product(id: UUID, db: AsyncSession = Depends(get_db)):
    data = await ProductService(db).get_product_by_id(id)
    data.pop("original_price") if data.get("original_price") else None
    data.pop("created_at")
    data.pop("updated_at")
    data.pop("deleted_at")
    return data


# ********** GET PRODUCT BY CATEGORY **********
@router.get(
    "/category/",
    description="This endpoint is used to get a product by category.",
    status_code=200,
)
async def get_product_by_category(
    parent_category: str | None = None,
    sub_category: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    if not parent_category and not sub_category:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Get Product By Parent Category Failed or Sub Category Failed!",
        )
    data = await ProductService(db).get_products_by_category(
        parent_category, sub_category
    )
    if not data:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Get Product By Category Failed!"
        )
    logging.warning(parent_category)
    logging.warning(sub_category)
    new_data = []
    for item in data:
        item.__dict__.pop("original_price") if item.__dict__.get(
            "original_price"
        ) else None
        new_data.append(item)
    return new_data


# ********** GET PRODUCT BY SLUG **********
@router.get(
    "/slug/{slug}",
    description="This endpoint is used to get a product by id.",
    status_code=200,
    responses={
        400: {"model": ResBadRequest, "description": "Not Found"},
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "tags": [],
                        "category": {
                            "slug": "category-1",
                            "parent_id": None,
                            "description": "Category 1 description",
                            "id": "6f4ffeb0-750f-49d3-ab4c-c2c8d8c4b343",
                            "name": "Category 1",
                        },
                        "country": "USA",
                        "thumbnail": "https://dev.image.customafk.com/products/iphone-13.jpeg",
                        "factory": "Apple",
                        "variant": None,
                        "name": "Iphone 13asdasd",
                        "status": "IN STOCK",
                        "preorder_start_date": None,
                        "preorder_end_date": None,
                        "sell_price": 900,
                        "quantity": 100,
                        "description": "This is a new product from Apple",
                        "slug": "iphone-13asdasd",
                        "id": "92792ee8-011b-4f9a-be7d-9f1c29eea149",
                    }
                }
            }
        },
    },
)
async def get_product_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    data = await ProductService(db).get_product_by_slug(slug)
    data.pop("original_price") if data.get("original_price") else None
    data.pop("created_at")
    data.pop("updated_at")
    data.pop("deleted_at")
    return data
