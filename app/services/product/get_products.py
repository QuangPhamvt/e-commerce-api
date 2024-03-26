from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD


class GetProducts:
    async def get_products(self, db: AsyncSession):
        return await ProductCRUD(db).get_products()
