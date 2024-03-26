from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import exchange_crud
from app.database.models import ExchangeRate


class GetList:
    @staticmethod
    async def get_list_exchange_rate(db: AsyncSession) -> Sequence[ExchangeRate]:
        return await exchange_crud.get_list_exchange(db)
