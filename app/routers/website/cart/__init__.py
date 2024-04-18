from uuid import UUID
from fastapi.routing import APIRouter
from app.configs.constants import CART, CART_PATH, CART_PREFIX
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.get_db import get_db
from app.dependencies.verify_access_token import get_me
from app.schemas.cart import CreateCartParam
from app.schemas.responses import Res201Resquest
from app.services.cart import CartService

"""
Web API Cart
"""

GET_CART_BY_USER = CART_PATH["GET_CART_BY_USER"]
CREATE_CART = CART_PATH["CREATE_CART"]
DELETE_CART = CART_PATH["DELETE_CART"]


router = APIRouter(prefix=CART_PREFIX, tags=[CART])


@router.post(
    CREATE_CART,
    description="This endpoint is used to create cart",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Add Product to Cart Succeed!", "model": Res201Resquest}
    },
)
async def create_cart(
    body: CreateCartParam, user_id=Depends(get_me), db: AsyncSession = Depends(get_db)
):
    return await CartService(db).create(body, user_id)


@router.get(
    GET_CART_BY_USER,
    description="This endpoint is used to get cart by user",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Get list cart succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "51babb32-40f4-4d14-bff2-4c035d09fcd0",
                            "user_id": "bc93610bfd214d259c186828d9116a8a",
                            "quantity": 3,
                            "description": "Category 1 description",
                            "product": {
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
                            },
                        }
                    ]
                }
            },
        }
    },
)
async def get_cart_by_user(user_id=Depends(get_me), db: AsyncSession = Depends(get_db)):
    return await CartService(db).read_by_user(user_id)


@router.delete(
    DELETE_CART,
    description="This endpoint is used to delete cart",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Delete Cart Succeed!", "model": Res201Resquest}},
)
async def delete_cart(
    id: UUID, user_id=Depends(get_me), db: AsyncSession = Depends(get_db)
):
    return await CartService(db).delete(id, user_id)
