from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import category_crud


class GetAll:
    async def get_all(self, db: AsyncSession):
        list_category = await category_crud.get_all(db)
        return list_category
