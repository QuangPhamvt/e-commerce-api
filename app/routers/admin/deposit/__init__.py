from uuid import UUID
from fastapi import APIRouter, Depends
from app.configs.constants import DEPOSIT, DEPOSIT_PATH, DEPOSIT_PREFIX
from app.dependencies.get_db import get_db
from app.schemas.deposit import (
    CreateDepositParams,
    ResCreateDeposit,
    UpdateDepositParams,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.responses import Res201Resquest
from app.services.deposit import DepositService

GET_LIST_DEPOSIT = DEPOSIT_PATH["GET_LIST_DEPOSIT"]
CREATE_DEPOSIT = DEPOSIT_PATH["CREATE_DEPOSIT"]
DELETE_DEPOSIT = DEPOSIT_PATH["DELETE_DEPOSIT"]
UPDATE_DEPOSIT = DEPOSIT_PATH["UPDATE_DEPOSIT"]
GET_DEPOSIT_BY_ID = DEPOSIT_PATH["GET_DEPOSIT_BY_ID"]

router = APIRouter(prefix=DEPOSIT_PREFIX, tags=[DEPOSIT])


@router.post(
    CREATE_DEPOSIT,
    description="This endpoint is used to create a new deposit type.",
    status_code=201,
    responses={
        201: {"description": "Create Deposit Succeed!", "model": ResCreateDeposit},
    },
)
async def create_deposit(body: CreateDepositParams, db: AsyncSession = Depends(get_db)):
    return await DepositService().create(body, db)


@router.put(
    UPDATE_DEPOSIT,
    description="This endpoint is used to update a product by id.",
    status_code=200,
    responses={
        200: {"description": "Update Deposit Type Succeed!", "model": Res201Resquest},
    },
)
async def update_product(
    id: UUID, body: UpdateDepositParams, db: AsyncSession = Depends(get_db)
):
    return await DepositService().update(id, body, db)


@router.get(
    GET_DEPOSIT_BY_ID,
    description="This endpoint is used to get a deposit type by id.",
    status_code=200,
    responses={
        200: {
            "description": "Get List Products Succeed!",
            "content": {
                "application/json": {
                    "example": {
                        "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                        "name": "Deposit 1",
                        "value": 0.7,
                        "fee": 0.01,
                    }
                }
            },
        }
    },
)
async def get_deposit_by_id(id: UUID, db: AsyncSession = Depends(get_db)):
    return await DepositService().get_by_id(id, db)


@router.get(
    GET_LIST_DEPOSIT,
    description="This endpoint is used to get list deposit types.",
    responses={
        200: {
            "description": "Get List Deposit Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "fff1d10a-e83b-4a04-8421-d6f56f726f9d",
                            "name": "Deposit 1",
                            "value": 0.7,
                            "fee": 0.01,
                        }
                    ]
                }
            },
        }
    },
)
async def get_list_deposit(db: AsyncSession = Depends(get_db)):
    return await DepositService().get_list_deposit(db)


@router.delete(
    DELETE_DEPOSIT,
    description="This endpoint is used to delete a deposit type by id.",
    responses={
        200: {
            "description": "Delete Deposit Type Succeed!",
            "model": Res201Resquest,
        },
    },
)
async def delete_deposit(id: UUID, db: AsyncSession = Depends(get_db)):
    return await DepositService().delete(id, db)
