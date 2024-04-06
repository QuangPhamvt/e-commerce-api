from uuid import UUID
from app.database.crud.user_crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.schemas.user import CreateUserParam


class Update:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_crud = UserCRUD(db)
    
    async def update_user(self, id: UUID, new_user: CreateUserParam):
        is_valid_id = await self.user_crud.read_user_by_id(id)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        await self.user_crud.update_user(id, new_user) #Chưa có hàm update_user
        return {"detail": "Update user succeed!"}