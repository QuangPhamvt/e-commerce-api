from fastapi import APIRouter
from app.configs.constants import (
    EXCHANGE,
    EXCHANGE_PATH,
    EXCHANGE_PREFIX,
)

from app.dependencies.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.services.exchange import ExchangeService

GET_LIST_EXCHANGE = EXCHANGE_PATH["GET_LIST_EXCHANGE"]
CREATE_EXCHANGE = EXCHANGE_PATH["CREATE_EXCHANGE"]
DELETE_EXCHANGE = EXCHANGE_PATH["DELETE_EXCHANGE"]
UPDATE_EXCHANGE = EXCHANGE_PATH["UPDATE_EXCHANGE"]
GET_EXCHANGE_BY_ID = EXCHANGE_PATH["GET_EXCHANGE_BY_ID"]


router = APIRouter(prefix=EXCHANGE_PREFIX, tags=[EXCHANGE])


@router.get(
    GET_LIST_EXCHANGE,
    description="This endpoint is used to get list exchange type.",
    responses={
        200: {
            "description": "Get List Exchange Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                            "currency": "USD",
                            "value": 0.7,
                        }
                    ]
                }
            },
        }
    },
)
async def get_list_exchange(db: AsyncSession = Depends(get_db)):
    return await ExchangeService().get_list_exchange_rate(db)
