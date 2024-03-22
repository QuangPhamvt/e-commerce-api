from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud.product_crud import ProductCRUD
from app.database.models import Product
from app.configs.Clounfront import get_image_from_url


class GetProducts:
    async def get_products(self, db: AsyncSession) -> Sequence[Product]:
        products = await ProductCRUD(db).get_products()
        new_products = self.__convert_image_to_url(products)
        products_exclude_sell_price = self.__convert_products_exclude_sell_price(
            new_products
        )
        return products_exclude_sell_price

    @staticmethod
    def __convert_image_to_url(products: Sequence[Product]) -> Sequence[Product]:
        for product in products:
            DOMAIN_IMAGE = get_image_from_url(product.image)
            if DOMAIN_IMAGE:
                product.image = DOMAIN_IMAGE

        return products

    @staticmethod
    def __convert_products_exclude_sell_price(
        products: Sequence[Product],
    ) -> Sequence[Product]:
        for product in products:
            product.__dict__.pop("sell_price")
        return products
