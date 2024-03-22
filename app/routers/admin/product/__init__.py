from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import PRODUCT, PRODUCT_PREFIX
from app.dependencies import get_db
from app.schemas.product import BodyCreateProduct, BodyUpdateProduct, ResCreateProduct
from app.schemas.responses import Res201Resquest
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
                            "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                            "name": "Iphone 13",
                            "description": "This is a new product from Apple",
                            "original_price": 1000,
                            "sell_price": 900,
                            "quantity": 100,
                            "image": "https://customafk-ecommerce-web.s3.amazonaws.com/products/iphone-13.webp",
                            "slug": "iphone-13",
                            "country": "USA",
                            "factory": "Apple",
                            "status": "active",
                            "category_id": None,
                            "series_id": None,
                            "created_at": "2024-03-20T23:13:55",
                            "updated_at": None,
                            "deleted_at": None,
                        }
                    ]
                }
            },
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
    return {"detail": f"Get Product {product_id} Succeed!"}


# ********** UPDATE PRODUCT BY ID **********
@router.put(
    "/{id}",
    description="This endpoint is used to update a product by id.",
    status_code=200,
    responses={
        200: {"description": "Update Product Succeed!", "model": Res201Resquest},
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
        200: {"description": "Delete Product Succeed!", "model": Res201Resquest},
    },
)
async def delete_product(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService().delete_by_Id(id=id, db=db)
