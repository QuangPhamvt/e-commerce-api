from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import PRODUCT, PRODUCT_PREFIX, PRODUCT_PATH
from app.dependencies import get_db
from app.schemas.product import (
    BodyCreateProduct,
    CreateProductResponse,
    ResCreateProduct,
    BodyUpdateProduct,
)
from app.schemas.responses import Res201Resquest, ResBadRequest
from app.services.product import ProductService

GET_LIST_PRODUCTS = PRODUCT_PATH["GET_LIST_PRODUCTS"]
CREATE_PRODUCT = PRODUCT_PATH["CREATE_PRODUCT"]
GET_PRODUCT = PRODUCT_PATH["GET_PRODUCT"]
UPDATE_PRODUCT = PRODUCT_PATH["UPDATE_PRODUCT"]
UPDATE_PRODUCT = PRODUCT_PATH["UPDATE_PRODUCT"]
DELETE_PRODUCT = PRODUCT_PATH["DELETE_PRODUCT"]
GET_PRODUCTS_BY_TAG = PRODUCT_PATH["GET_PRODUCTS_BY_TAG"]
SET_SERIES_TO_PRODUCT = PRODUCT_PATH["SET_SERIES_TO_PRODUCT"]
SET_CATEGORY_TO_PRODUCT = PRODUCT_PATH["SET_CATEGORY_TO_PRODUCT"]
GET_PRODUCTS_BY_SERIES = PRODUCT_PATH["GET_PRODUCTS_BY_SERIES"]


router = APIRouter(
    prefix=PRODUCT_PREFIX,
    tags=[PRODUCT],
)


# ********** GET LIST PRODUCTS **********
@router.get(
    GET_LIST_PRODUCTS,
    description="This endpoint is used to get list of products.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Products Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                            "name": "Iphone 13",
                            "description": "This is a new product from Apple",
                            "original_price": 1000,
                            "sell_price": 900,
                            "quantity": 100,
                            "thumbnail": "https://dev.customafk.com/products/iphone-13.jpeg",
                            "slug": "iphone-13",
                            "country": "USA",
                            "factory": "Apple",
                            "status": "active",
                            "category_id": None,
                            "series_id": None,
                            "variant": "string",
                            "created_at": "2024-03-20T23:13:55",
                            "updated_at": None,
                            "deleted_at": None,
                            "preoder_start_date": "2024-03-20T23:13:55",
                            "preoder_end_date": "2024-03-20T23:13:55",
                        }
                    ]
                }
            },
        },
    },
)
async def get_list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService(db).get_all()


# ********** CREATE PRODUCT **********
@router.post(
    CREATE_PRODUCT,
    description="This endpoint is used to create a new product.",
    status_code=201,
    responses={
        201: {"model": ResCreateProduct},
    },
)
async def create_product(body: BodyCreateProduct, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).create_product(body)


# ********** GET PRODUCT BY ID **********
@router.get(
    GET_PRODUCT,
    description="This endpoint is used to get a product by id.",
    status_code=200,
    responses={
        400: {"model": ResBadRequest, "description": "Not Found"},
        200: {
            "id": "92792ee8-011b-4f9a-be7d-9f1c29eea149",
            "name": "Iphone 13",
            "thumbnail": "https://dev.image.customafk.com/products/iphone-13.jpeg",
            "country": "USA",
            "factory": "Apple",
            "slug": "category-1",
            "tags": [
                {
                    "name": "Tag 1",
                    "deleted_at": "string",
                    "id": "f837cf6a-4be1-4302-9df9-84a7ba320bbd",
                }
            ],
            "variant": "string",
            "sell_price": 900,
            "original_price": 1000,
            "preorder_start_date": "string",
            "preorder_end_date": "string",
            "status": "IN STOCK",
            "quantity": 100,
            "description": "This is a new product from Apple",
        },
    },
)
async def get_product(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).get_product_by_id(id)


# ********** UPDATE PRODUCT BY ID **********
@router.put(
    UPDATE_PRODUCT,
    description="This endpoint is used to update a product by id.",
    status_code=200,
    responses={
        200: {"description": "Update Product Succeed!", "model": Res201Resquest},
    },
)
async def update_product(
    id: UUID, body: BodyUpdateProduct, db: AsyncSession = Depends(get_db)
):
    return await ProductService(db).update_by_id(id, body)


# ********** DELETE PRODUCT BY ID **********
@router.delete(
    DELETE_PRODUCT,
    response_description="This endpoint is used to delete a product by id.",
    status_code=200,
    responses={
        200: {"description": "Delete Product Succeed!", "model": Res201Resquest},
    },
)
async def delete_product(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).delete_by_id(id)


# ********** GET LIST PRODUCTS BY TAG **********
@router.get(
    GET_PRODUCTS_BY_TAG,
    response_description="This endpoint is used to get a list product by tag name.",
    status_code=200,
    response_model=list[CreateProductResponse],
    responses={
        200: {
            "description": "Get List Products By Tag Succeed!",
        },
        400: {"description": "Tag not found!"},
    },
)
async def get_list_products_by_tag(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).get_products_by_tag(id)


# ********** SET SERIES TO PRODUCT **********
@router.put(
    SET_SERIES_TO_PRODUCT,
    response_description="This endpoint is used to set series to product.",
    status_code=201,
    responses={
        201: {"description": "Set series to product succeed!", "model": Res201Resquest}
    },
)
async def set_series_to_product(
    product_id: UUID, series_id: UUID, db: AsyncSession = Depends(get_db)
):
    return await ProductService(db).set_series_to_product(product_id, series_id)


# ********** SET CATEGORY TO PRODUCT **********
@router.put(
    SET_CATEGORY_TO_PRODUCT,
    response_description="This endpoint is used to set category to product.",
    status_code=201,
    responses={
        201: {
            "description": "Set category to product succeed!",
            "model": Res201Resquest,
        }
    },
)
async def set_category_to_product(
    product_id: UUID, category_id: UUID, db: AsyncSession = Depends(get_db)
):
    return await ProductService(db).set_category_to_product(product_id, category_id)


# ********** GET LIST PRODUCTS BY SERIES **********
@router.get(
    GET_PRODUCTS_BY_SERIES,
    response_description="This endpoint is used to get list of products by series.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Products Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                            "name": "Iphone 13",
                            "description": "This is a new product from Apple",
                            "original_price": 1000,
                            "sell_price": 900,
                            "quantity": 100,
                            "thumbnail": "https://dev.customafk.com/products/iphone-13.jpeg",
                            "slug": "iphone-13",
                            "country": "USA",
                            "factory": "Apple",
                            "status": "active",
                            "category_id": None,
                            "series_id": None,
                            "variant": "string",
                            "created_at": "2024-03-20T23:13:55",
                            "updated_at": None,
                            "deleted_at": None,
                            "preoder_start_date": "2024-03-20T23:13:55",
                            "preoder_end_date": "2024-03-20T23:13:55",
                        }
                    ]
                }
            },
        },
    },
)
async def get_products_by_series(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService(db).get_products_by_series(id)
