from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import PRODUCT, PRODUCT_PREFIX
from app.dependencies import get_db
from app.schemas.product import BodyCreateProduct, BodyUpdateProduct, ResCreateProduct
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
async def get_list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService().get_products(db)


# ********** CREATE PRODUCT **********
@router.post(
    "",
    description="This endpoint is used to create a new product.",
    status_code=201,
    responses={
        201: {"model": ResCreateProduct},
    },
)
async def create_product(body: BodyCreateProduct, db: AsyncSession = Depends(get_db)):
    return await ProductService().create_product(body, db)


# ********** GET PRODUCT BY ID **********
@router.get(
    "/{id}",
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
    "/{id}",
    description="This endpoint is used to update a product by id.",
    status_code=200,
    responses={
        200: {
            "description": "Update Product Succeed!",
        },
    },
)
async def update_product(
    id: UUID, body: BodyUpdateProduct, db: AsyncSession = Depends(get_db)
):
    return await ProductService().update_product_by_id(id, body, db)


# ********** DELETE PRODUCT BY ID **********
@router.delete(
    "/{id}",
    response_description="This endpoint is used to delete a product by id.",
    status_code=200,
    responses={
        200: {
            "description": "Delete Product Succeed!",
        },
    },
)
async def delete_product(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService().delete_by_Id(id=id, db=db)
