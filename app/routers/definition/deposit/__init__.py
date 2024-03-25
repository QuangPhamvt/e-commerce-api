from fastapi import APIRouter
from app.configs.constants import DEPOSIT, DEPOSIT_PATH, DEPOSIT_PREFIX
from app.dependencies.get_db import get_db
from app.services.deposit import DepositService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

GET_LIST_DEPOSIT = DEPOSIT_PATH["GET_LIST_DEPOSIT"]
CREATE_DEPOSIT = DEPOSIT_PATH["CREATE_DEPOSIT"]
DELETE_DEPOSIT = DEPOSIT_PATH["DELETE_DEPOSIT"]
UPDATE_DEPOSIT = DEPOSIT_PATH["UPDATE_DEPOSIT"]
GET_DEPOSIT_BY_ID = DEPOSIT_PATH["GET_DEPOSIT_BY_ID"]

router = APIRouter(prefix=DEPOSIT_PREFIX, tags=[DEPOSIT])


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
