import logging
from uuid import UUID
from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.Clounfront import get_image_from_url
from app.configs.S3.delete_object import delete_object_s3
from app.configs.S3.put_object import put_object
from app.database.crud.category_crud import CategoryCRUD
from app.database.crud.series_crud import SeriesCRUD
from app.database.crud.tag_crud import TagCRUD
from app.database.crud.product_crud import ProductCRUD
from app.database.crud.product_tag_crud import ProductTagCRUD
from app.database.models.Product import Product
from app.schemas.product import BodyCreateProduct, BodyUpdateProduct, ProductCreateCRUD
from app.utils.helper import helper


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tag_crud = TagCRUD(db)
        self.product_crud = ProductCRUD(db)
        self.category_crud = CategoryCRUD(db)
        self.product_tag_crud = ProductTagCRUD(db)
        self.series_crud = SeriesCRUD(db)

    async def get_all(self):
        """
        Get all products
        Parameters: None
        """
        products = await self.product_crud.read_all()
        for product in products:
            product.thumbnail = helper.convert_image_to_url(product.thumbnail)
        return products

    async def get_products_by_tag(self, id: UUID):
        products = await self.product_tag_crud.read_by_tag(id)
        return products

    async def get_product_by_id(self, id: UUID):
        try:
            product = await self.product_crud.read_by_id(id)
            if not product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Id not found!",
                )

            tags = await self.product_tag_crud.read_list_tags_by_product(product.id)
            category = None
            series = None

            if product.category_id:
                category = await self.category_crud.read_by_id(product.category_id)
            if product.series_id:
                series = await self.series_crud.get_by_id(product.series_id)

            product.__dict__.pop("category_id")
            product.thumbnail = self.__convert_image_to_url(product)
            new_product = {
                "tags": tags,
                "category": category if category else None,
                "series": series if series else None,
                **product.__dict__,
            }
            return new_product
        except Exception as e:
            logging.warning(e)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Failed to get product",
            )

    async def create_product(self, body: BodyCreateProduct):
        try:
            slug = helper.slugify(body.name)
            type = body.thumbnail_type

            await self.__check_product_exist(slug)

            url = f"products/{slug}.{type}"
            new_product = ProductCreateCRUD(thumbnail=url, **body.model_dump())

            product_id = await self.product_crud.create(new_product)
            await self.product_tag_crud.create_many_by_product_id(product_id, body.tags)
            data = self.__create_presigned_url("customafk-ecommerce-web", slug, type)

            if data is None:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
                )
            return {"detail": "Product created successfully", "presigned_url": data}
        except Exception as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to create product : {e}"
            )

    async def update_by_id(self, id: UUID, body: BodyUpdateProduct):
        try:
            await self.product_crud.update_by_id(id, body)
            return {"detail": f"Update Product {id} Succeed!"}
        except Exception as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to update product : {e}"
            )

    async def delete_by_id(self, id: UUID):
        try:
            product = await self.product_crud.read_by_id(id)

            if not product:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

            self.__delete_image_S3(product.thumbnail)
            await self.product_crud.delete_by_id(id)

            return {"detail": "Product deleted"}
        except Exception as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to delete product : {e}"
            )

    async def set_category_to_product(self, product_id: UUID, category_id: UUID):
        try:
            product = await self.product_crud.read_by_id(product_id)
            if not product:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
            category = await self.category_crud.read_by_id(category_id)
            if not category:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")

            await self.product_crud.update_category_to_product(product_id, category.id)
            return {"detail": "Set series to product succeed!"}
        except Exception as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to set category to product : {e}"
            )

    async def set_series_to_product(self, product_id: UUID, series_id: UUID):
        product = await self.product_crud.read_by_id(product_id)
        if not product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
        series = await self.series_crud.get_by_id(series_id)
        if not series:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")

        await self.product_crud.update_series_to_product(product_id, series_id)
        return {"detail": "Set series to product succeed!"}

    async def get_products_by_series(self, series_id: UUID) -> Sequence[Product]:
        series = await self.series_crud.get_by_id(series_id)
        if not series:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")
        products = await self.product_crud.read_product_by_series(series_id)
        for product in products:
            product.thumbnail = helper.convert_image_to_url(product.thumbnail)
        return products

    async def __check_product_exist(self, slug: str):
        product = await self.product_crud.read_by_slug(slug)
        if product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product already exists!")
        pass

    @staticmethod
    def __create_presigned_url(bucket_name: str, slug: str, image_type: str):
        url = f"products/{slug}.{image_type}"
        type = f"image/{image_type}"
        return put_object(bucket_name, url, type)

    @staticmethod
    def __convert_image_to_url(product: Product) -> str:
        DOMAIN_IMAGE = get_image_from_url(product.thumbnail)
        if DOMAIN_IMAGE:
            product.thumbnail = DOMAIN_IMAGE

        return product.thumbnail

    async def __get_tag_id(self, tag_name: str):
        tag_id = await self.tag_crud.is_exist_name(tag_name)
        if not tag_id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tag not found!")
        return tag_id

    @staticmethod
    def __delete_image_S3(thumbnail: str):
        res = delete_object_s3("customafk-ecommerce-web", thumbnail)
        return res
