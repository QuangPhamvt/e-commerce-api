from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import category_crud


class GetAll:
    async def get_all(db: AsyncSession):
        list_category = await category_crud.get_all(db=db)
        return list_category
