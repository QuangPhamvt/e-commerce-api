from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import tag_crud


class GetAll:
    async def get_all(self, db: AsyncSession):
        tags = await tag_crud.get_all(db)
        return tags
