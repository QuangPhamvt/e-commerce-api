from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import PRODUCT, PRODUCT_PREFIX
from app.dependencies import get_db
from app.schemas.product import ProductCreate
from app.routers.product.services import ProductService


router = APIRouter(
    prefix=PRODUCT_PREFIX,
    tags=[PRODUCT],
)


# ********** GET LIST PRODUCTS **********
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


# ********** CREATE PRODUCT **********
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
async def create_product(body: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductService().create_product(body, db)


# ********** GET PRODUCT BY ID **********
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


# ********** UPDATE PRODUCT BY ID **********
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


# ********** DELETE PRODUCT BY ID **********
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
