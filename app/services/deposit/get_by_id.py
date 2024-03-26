from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import deposit_crud


class GetById:
    @staticmethod
    async def get_by_id(id: UUID, db: AsyncSession):
        deposit = await deposit_crud.get_deposit_type_by_id(id, db)
        if not deposit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        return deposit
