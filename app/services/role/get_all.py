from app.database.crud import role_crud
from sqlalchemy.ext.asyncio import AsyncSession


class GetAll:
    @staticmethod
    async def get_all(db: AsyncSession):
        return await role_crud.get_list_role(db=db)
