from uuid import UUID
from fastapi import APIRouter
from app.configs.constants import (
    EXCHANGE,
    EXCHANGE_PATH,
    EXCHANGE_PREFIX,
)
from app.schemas.exchange import (
    CreateExchangeParams,
    ResCreateExchange,
    UpdateExchangeParams,
)
from app.dependencies.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.schemas.responses import Res201Resquest
from app.services.exchange import ExchangeService

GET_LIST_EXCHANGE = EXCHANGE_PATH["GET_LIST_EXCHANGE"]
CREATE_EXCHANGE = EXCHANGE_PATH["CREATE_EXCHANGE"]
DELETE_EXCHANGE = EXCHANGE_PATH["DELETE_EXCHANGE"]
UPDATE_EXCHANGE = EXCHANGE_PATH["UPDATE_EXCHANGE"]
GET_EXCHANGE_BY_ID = EXCHANGE_PATH["GET_EXCHANGE_BY_ID"]


router = APIRouter(prefix=EXCHANGE_PREFIX, tags=[EXCHANGE])


@router.post(
    CREATE_EXCHANGE,
    description="This endpoint is used to create a new exchange type.",
    status_code=201,
    responses={
        201: {
            "description": "Create Exchange Type Succeed!",
            "model": ResCreateExchange,
        },
    },
)
async def create_exchange_type(
    body: CreateExchangeParams, db: AsyncSession = Depends(get_db)
):
    return await ExchangeService().create(body, db)


@router.put(
    UPDATE_EXCHANGE,
    description="This endpoint is used to update a exchange type by id.",
    status_code=200,
    responses={
        200: {"description": "Update Exchange Type Succeed!", "model": Res201Resquest},
    },
)
async def update_exchange_type(
    id: UUID, body: UpdateExchangeParams, db: AsyncSession = Depends(get_db)
):
    return await ExchangeService().update(id, body, db)


@router.get(
    GET_EXCHANGE_BY_ID,
    description="This endpoint is used to get a exchange type by id.",
    status_code=200,
    responses={
        200: {
            "description": "Get Exchange Type Succeed!",
            "content": {
                "application/json": {
                    "example": {
                        "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                        "currency": "USD",
                        "value": 0.7,
                    }
                }
            },
        }
    },
)
async def get_exchange_type_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ExchangeService().get_by_id(id, db)


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


@router.delete(
    DELETE_EXCHANGE,
    description="This endpoint is used to delete a exchange type by id.",
    responses={
        200: {
            "description": "Delete Exchange Type Succeed!",
            "model": Res201Resquest,
        },
    },
)
async def delete_exchange(id: UUID, db: AsyncSession = Depends(get_db)):
    return await ExchangeService().delete(id, db)
