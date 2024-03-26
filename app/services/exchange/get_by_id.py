from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import exchange_crud


class GetById:
    @staticmethod
    async def get_by_id(id: UUID, db: AsyncSession):
        exchange_rate = await exchange_crud.get_exchange_rate_by_id(id, db)
        if not exchange_rate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        return exchange_rate
