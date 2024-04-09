from typing import Sequence
from uuid import UUID
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
from app.database.crud.products_image_crud import ProductsImageCRUD
from app.database.models.Product import Product
from app.schemas.product import (
    CreateProductsImageBody,
    BodyCreateProduct,
    BodyUpdateProduct,
    ProductCreateCRUD,
    ImageType,
)
from app.utils.helper import helper
import logging


class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.tag_crud = TagCRUD(db)
        self.product_crud = ProductCRUD(db)
        self.category_crud = CategoryCRUD(db)
        self.product_tag_crud = ProductTagCRUD(db)
        self.series_crud = SeriesCRUD(db)
        self.products_image_crud = ProductsImageCRUD(db)

    async def get_all(self):
        products = await self.product_crud.read_all()
        for product in products:
            product.thumbnail = helper.convert_image_to_url(product.thumbnail)
        return products

    async def get_products_by_tag(self, tag_name: str):
        tag_id = await self.__get_tag_id(tag_name)
        products = await self.product_tag_crud.read_by_tag(tag_id)
        return products

    async def get_product_by_id(self, id: UUID):
        try:
            product = await self.product_crud.read_by_id(id)
            if not product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Id not found!",
                )
            tags = await self.product_tag_crud.read_list_tags_by_product(id)

            category = None
            if product.category_id:
                category = await self.category_crud.read_by_id(product.category_id)
            series = None
            if product.series_id:
                series = await self.series_crud.get_by_id(product.series_id)

            images = await self.products_image_crud.get_list_image_urls(id)

            product.__dict__.pop("category_id")
            product.thumbnail = self.__convert_image_to_url(product)
            new_product = {
                "tags": tags,
                "category": category if category else None,
                "series": series if series else None,
                "images": images,
                **product.__dict__,
            }
            return new_product
        except Exception as e:
            logging.warning(f"Error getting product by id : {e}")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Failed to get product",
            )

    async def create_product(self, body: BodyCreateProduct):
        slug = helper.slugify(body.name)
        type = body.thumbnail_type

        await self.__check_product_exist(slug)

        url = f"products/{slug}.{type}"
        new_product = ProductCreateCRUD(thumbnail=url, **body.model_dump())
        await self.product_crud.create(new_product)

        data = self.__create_presigned_url("customafk-ecommerce-web", slug, type)

        if data is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
            )
        return {"detail": "Product created successfully", "presigned_url": data}

    async def update_by_id(self, id: UUID, body: BodyUpdateProduct):
        await self.product_crud.update_by_id(id, body)
        return {"detail": f"Update Product {id} Succeed!"}

    async def delete_by_id(self, id: UUID):
        product = await self.product_crud.read_by_id(id)

        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

        self.__delete_image_S3(product.thumbnail)
        await self.product_crud.delete_by_id(id)

        return {"detail": "Product deleted"}

    async def __check_product_exist(self, slug: str):
        product = await self.product_crud.read_by_slug(slug)
        if product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product already exists!")
        pass

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

    async def create_product_images(self, id: UUID, images: list[ImageType]):
        try:
            is_valid_product = await self.product_crud.read_by_id(id)
            if not is_valid_product:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
            slug = await self.product_crud.get_product_slug(id)

            exist_images_quantity = await self.products_image_crud.images_quantity(id)
            is_exceed = self.__check_image_quantity(len(images), exist_images_quantity)
            if is_exceed:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Image quantity exceed! Each product has only 5 images!",
                )

            presigned_urls = []
            for image in images:
                image_slug = f"{slug}-{image.order.value}"
                image_url = f"products/{image_slug}.{image.type}"
                new_product_image = CreateProductsImageBody(
                    slug=image_slug, image_url=image_url, product_id=id
                )
                await self.products_image_crud.create(new_product_image)
                data = self.__create_presigned_url(
                    "customafk-ecommerce-web", image_slug, image.type
                )
                if data is None:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
                    )
                presigned_urls.append(data)
            return {
                "detail": "Product Image created successfully",
                "result_url": "http://127.0.0.1:8000/api/v1/admin/products/{id}/images/1",
            }
        except Exception:
            return {
                "detail": "Product Image creation failed",
                "result_url": "http://127.0.0.1:8000/api/v1/admin/products/{id}/images/0",
            }

    async def delete_product_image(self, id: UUID, slug: str):
        is_valid_product = await self.product_crud.read_by_id(id)
        if not is_valid_product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
        is_valid_id = await self.products_image_crud.get_product_image_id_by_slug(slug)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Product Image slug not found!"
            )
        await self.products_image_crud.delete(is_valid_id)
        return {"detail": "Product Image deleted successfully"}

    async def update_product_image(self, id: UUID, slug: str, body: ImageType):
        is_valid_product = await self.product_crud.read_by_id(id)
        if not is_valid_product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
        is_valid_id = await self.products_image_crud.get_product_image_id_by_slug(slug)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Product Image slug not found!"
            )

        slug = await self.product_crud.get_product_slug(id)
        image_slug = f"{slug}-{body.order.value}"
        image_url = f"products/{image_slug}.{body.type}"
        await self.products_image_crud.update(is_valid_id, image_slug, image_url)
        return {"detail": "Product Image updated successfully"}

    @staticmethod
    def __check_image_quantity(new_images_quantity: int, exist_images_quatity: int):
        return new_images_quantity > 5 - exist_images_quatity

    async def check_product_image_creation(self, id: UUID, result: int):
        images = await self.products_image_crud.get_product_images(id)
        if result == 0:
            [self.__delete_image_S3(image.image_url) for image in images]
            await self.products_image_crud.delete_by_product_id(id)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create product images"
            )
        presigned_urls = []
        for image in images:
            url = self.__create_presigned_url(
                "customafk-ecommerce-web", image.slug, image.image_url[-3:]
            )
            if url is None:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
                )
            presigned_urls.append(url)
        return {
            "detail": {"Product Image created successfully"},
            "presigned_urls": presigned_urls,
        }
