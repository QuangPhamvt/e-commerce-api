from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs.constants import PRODUCT, PRODUCT_PREFIX
from app.schemas.product import GetListProduct
from app.dependencies import get_db
from app.schemas.responses import ResBadRequest
from app.services.product import ProductService
from app.schemas.product import CreateProductResponse

router = APIRouter(
    prefix=PRODUCT_PREFIX,
    tags=[PRODUCT],
)


# ********** GET LIST PRODUCTS **********
@router.get(
    "",
    description="This endpoint is used to get list of products.",
    status_code=200,
    response_model=list[GetListProduct],
    responses={
        200: {
            "description": "Get List Products Succeed!",
        },
    },
)
async def get_list_products(db: AsyncSession = Depends(get_db)):
    return await ProductService().get_products(db)


# ********** GET PRODUCT BY ID **********
@router.get(
    "/{id}",
    description="This endpoint is used to get a product by id.",
    status_code=200,
    response_model=CreateProductResponse,
    responses={
        400: {"model": ResBadRequest, "description": "Not Found"},
    },
)
async def get_product(id: str, db: AsyncSession = Depends(get_db)):
    return await ProductService().get_product_by_id(id, db)
