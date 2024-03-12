from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD

from app.schemas.product import ProductCreate


class CreateProduct:
    async def create_product(self, body: ProductCreate, db: AsyncSession):
        return await ProductCRUD(db).create(body)
