from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD
from app.utils.helper import helper
from fastapi import HTTPException, status


class GetProductById:
    async def get_product_by_id(self, id: str, db: AsyncSession):
        product_id = helper.convert_str_to_UUID(id)
        product = await ProductCRUD(db).get_product_by_id(product_id)
        if not product:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        product.thumbnail = helper.convert_image_to_url(product.thumbnail)
        return product
