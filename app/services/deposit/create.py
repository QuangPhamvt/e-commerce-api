from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import deposit_crud
from app.schemas.deposit import CreateDepositData, CreateDepositParams


class Create:
    async def create(self, body: CreateDepositParams, db: AsyncSession):
        is_exist_value = await self.__is_exist_name(body.name, db)
        if is_exist_value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Value already exist"
            )
        data = CreateDepositData(**body.model_dump())
        await deposit_crud.create_deposit_type(data, db)
        return {"detail": "Create deposit type succeed!"}

    @staticmethod
    async def __is_exist_name(name: str, db: AsyncSession):
        return await deposit_crud.is_exist_name(name, db)
