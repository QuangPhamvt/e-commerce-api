from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.user_crud import UserCRUD


class GetById:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_crud = UserCRUD(db)

    @staticmethod
    async def get_by_id(id: UUID, db: AsyncSession):
        user_detail = await UserCRUD.read_user_by_id()
        return user_detail
