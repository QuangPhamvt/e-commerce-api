from uuid import UUID
from app.database.crud.user_crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status


class Delete:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_crud = UserCRUD(db)
    
    async def delete_user(self, id: UUID):
        is_valid_id = await self.user_crud.read_user_by_id(id)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        await self.user_crud.delete_user(id) #Chưa có hàm delete_user
        return {"detail": "Delete user succeed!"}