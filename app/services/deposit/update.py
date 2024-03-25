from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import deposit_crud
from app.schemas.deposit import UpdateDepositData, UpdateDepositParams


class Update:
    async def update(self, id: UUID, body: UpdateDepositParams, db: AsyncSession):
        await self.__is_valid_data(id, body, db)
        data = UpdateDepositData(**body.model_dump())
        await deposit_crud.update_deposit_type(id, data, db)
        return {"detail": f"Update Deposit {id} Succeed!"}

    @staticmethod
    async def __is_valid_data(id: UUID, data: UpdateDepositParams, db: AsyncSession):
        is_valid_id = await deposit_crud.get_deposit_type_by_id(id, db)
        if not is_valid_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        is_exist_name = await deposit_crud.is_exist_name(data.name, db)
        print(is_exist_name)
        print(id)
        if is_exist_name and is_exist_name != id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name already exist!"
            )
        pass
