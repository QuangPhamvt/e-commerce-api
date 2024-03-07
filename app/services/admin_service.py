from app.database.crud import user_crud, customer_address_crud
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

class AdminService:
    @staticmethod
    async def get_list_users(db: AsyncSession):
        list_users = await user_crud.get_list_users(db=db)
        return list_users

admin_service: AdminService = AdminService()