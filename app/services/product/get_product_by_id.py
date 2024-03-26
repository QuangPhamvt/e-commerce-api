from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD
from app.utils.helper import Helper
from fastapi import HTTPException, status


class GetProductById:
    async def get_product_by_id(self, id: str, db: AsyncSession):
        product_id = Helper.convert_str_to_UUID(id)
        is_valid_id = await ProductCRUD(db).get_product_by_id(product_id)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        return is_valid_id
