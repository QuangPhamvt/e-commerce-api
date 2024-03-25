from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import exchange_crud
from app.schemas.exchange import UpdateExchangeData, UpdateExchangeParams


class Update:
    async def update(self, id: UUID, body: UpdateExchangeParams, db: AsyncSession):
        await self.__is_valid_data(id, body, db)
        data = UpdateExchangeData(**body.model_dump())
        await exchange_crud.update_exchange_rate(id, data, db)
        return {"detail": f"Update Exchange Rate {id} Succeed!"}

    @staticmethod
    async def __is_valid_data(id: UUID, data: UpdateExchangeParams, db: AsyncSession):
        is_valid_id = await exchange_crud.get_exchange_rate_by_id(id, db)
        if not is_valid_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        is_exist_currency = await exchange_crud.is_exist_currency(data.currency, db)
        if is_exist_currency and is_exist_currency != id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Currency already exist!",
            )
        pass
