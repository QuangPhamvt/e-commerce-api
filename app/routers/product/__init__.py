from uuid import UUID
from fastapi import APIRouter

from app.configs.constants import PRODUCT, PRODUCT_PREFIX


router = APIRouter(
    prefix=PRODUCT_PREFIX,
    tags=[PRODUCT],
)


@router.get(
    "/",
    description="This endpoint is used to get list of products.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Products Succeed!",
        },
    },
)
async def get_list_products():
    return {"message": "Get List Products Succeed!"}


@router.post(
    "/",
    description="This endpoint is used to create a new product.",
    status_code=201,
    responses={
        201: {
            "description": "Create Product Succeed!",
        },
    },
)
async def create_product():
    return {"message": "Create Product Succeed!"}


@router.get(
    "/{product_id}",
    description="This endpoint is used to get a product by id.",
    status_code=200,
    responses={
        200: {
            "description": "Get Product Succeed!",
        },
    },
)
async def get_product(product_id: UUID):
    return {"message": f"Get Product {product_id} Succeed!"}


@router.put(
    "/{product_id}",
    description="This endpoint is used to update a product by id.",
    status_code=200,
    responses={
        200: {
            "description": "Update Product Succeed!",
        },
    },
)
async def update_product(product_id: UUID):
    return {"message": f"Update Product {product_id} Succeed!"}


@router.delete(
    "/{product_id}",
    response_description="This endpoint is used to delete a product by id.",
    status_code=200,
    responses={
        200: {
            "description": "Delete Product Succeed!",
        },
    },
)
async def delete_product(product_id: UUID):
    return {"message": f"Delete Product {product_id} Succeed!"}
