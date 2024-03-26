from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import exchange_crud
from app.schemas.exchange import CreateExchangeData, CreateExchangeParams


class Create:
    async def create(self, body: CreateExchangeParams, db: AsyncSession):
        is_exist_value = await self.__is_exist_currency(body.currency, db)
        if is_exist_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Currency already exist"
            )
        data = CreateExchangeData(**body.model_dump())
        await exchange_crud.create_exchange_rate(data, db)
        return {"detail": "Create exchange rate succeed!"}

    @staticmethod
    async def __is_exist_currency(currency: str, db: AsyncSession):
        return await exchange_crud.is_exist_currency(currency, db)
