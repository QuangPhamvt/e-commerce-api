from app.database.crud import user_crud
from sqlalchemy.ext.asyncio import AsyncSession


class GetList:
    @staticmethod
    async def get_list_users(db: AsyncSession):
        list_users = await user_crud.get_list_users(db=db)
        return list_users
