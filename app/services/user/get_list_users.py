from app.database.crud import user_crud
from sqlalchemy.ext.asyncio import AsyncSession


class GetList:
    async def get_list_users(self, db: AsyncSession):
        list_users = await user_crud.UserCRUD(db).read_list_users()
        return list_users
