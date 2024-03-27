from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD
from app.utils.helper import helper


class GetProducts:
    async def get_products(self, db: AsyncSession):
        products = await ProductCRUD(db).get_products()
        for product in products:
            product.thumbnail = helper.convert_image_to_url(product.thumbnail)
        return products
