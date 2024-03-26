from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import deposit_crud
from app.database.models.Product import DepositType


class GetList:
    @staticmethod
    async def get_list_deposit(db: AsyncSession) -> Sequence[DepositType]:
        return await deposit_crud.get_list_deposit(db)
