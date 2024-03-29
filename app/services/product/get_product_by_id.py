from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.Clounfront import get_image_from_url
from app.database.crud import product_tag_crud
from app.database.crud.product_crud import ProductCRUD
from app.database.models import Product
from fastapi import HTTPException, status


class GetProductById:
    async def get_product_by_id(self, id: UUID, db: AsyncSession):
        try:
            product = await ProductCRUD(db).get_product_by_id(id)
            if not product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Id not found!",
                )

            product.thumbnail = self.__convert_image_to_url(product)
            tags = await product_tag_crud.get_list_tags_by_product(id, db)
            new_product = {
                "tags": tags,
                **product.__dict__,
            }
            return new_product
        except Exception:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Failed to get product",
            )

    @staticmethod
    def __convert_image_to_url(product: Product) -> str:
        DOMAIN_IMAGE = get_image_from_url(product.thumbnail)
        if DOMAIN_IMAGE:
            product.thumbnail = DOMAIN_IMAGE

        return product.thumbnail
