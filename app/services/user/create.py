
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.user_crud import UserCRUD
from app.schemas.user import CreateUserParam


class Create:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_crud = UserCRUD(db)
    
    async def create_user(self, user: CreateUserParam):
        is_exist_user = await self.user_crud.read_user_by_id(user.id)
        if is_exist_user:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "This user already exist!",
            )
        await self.user_crud.create_user(user)
        return {"detail": "Create user succeed!"}