from uuid import UUID
from app.database.crud import deposit_crud
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


class Delete:
    @staticmethod
    async def delete(id: UUID, db: AsyncSession):
        is_valid_id = await deposit_crud.get_deposit_type_by_id(id, db)
        if not is_valid_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!"
            )
        await deposit_crud.delete_deposit_type_by_id(id, db)
        return {"detail": "Delete deposit type succeed!"}
