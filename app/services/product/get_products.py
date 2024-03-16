from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD
from app.database.models import Product
from app.configs.S3.get_object import get_object


class GetProducts:
    async def get_products(self, db: AsyncSession) -> Sequence[Product]:
        products = await ProductCRUD(db).get_products()
        new_products = self.__convert_image_to_url(products)
        return new_products

    @staticmethod
    def __convert_image_to_url(products: Sequence[Product]) -> Sequence[Product]:
        for product in products:
            DOMAIN_IMAGE = get_object("customafk-ecommerce-web", product.image)
            if DOMAIN_IMAGE:
                product.image = DOMAIN_IMAGE

        return products
