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

    async def get_products_by_category(
        self, parent_category: str | None, sub_category: str | None
    ):
        try:
            products = []
            if parent_category:
                category = await self.category_crud.read_by_slug(parent_category)
                if not category:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, "Category not found!"
                    )
                products = await self.product_crud.read_by_parent_category(category.id)
                return products
            if sub_category:
                category = await self.category_crud.read_by_slug(sub_category)
                if not category:
                    raise HTTPException(
                        status.HTTP_400_BAD_REQUEST, "Category not found!"
                    )
                products = await self.product_crud.read_by_sub_category(category.id)

            for product in products:
                product.thumbnail = helper.convert_image_to_url(product.thumbnail)
            return products
        except Exception as e:
            HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to get product by category : {e}"
            )

    async def get_product_by_slug(self, slug: str):
        try:
            category = None
            series = None
            product = await self.product_crud.read_by_slug(slug)
            if not product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Id not found!",
                )
            tags = await self.product_tag_crud.read_list_tags_by_product(product.id)

            if product.category_id:
                category = await self.category_crud.read_sub_with_parent_by_id(
                    product.category_id
                )
            if product.series_id:
                series = await self.series_crud.get_by_id(product.series_id)
                series.__dict__.pop("created_at")
                series.__dict__.pop("updated_at")
                series.__dict__.pop("deleted_at")
                if series is not None and series.image is not None:
                    series.image = helper.convert_image_to_url(series.image)

            images = await self.products_image_crud.get_list_image_urls(product.id)
            images = [get_image_from_url(image) for image in images]

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
            logging.warning(e)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Failed to get product {e}",
            )

    async def get_product_by_id(self, id: UUID):
        try:
            category = None
            series = None
            product = await self.product_crud.read_by_id(id)
            if not product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "Id not found!",
                )
            tags = await self.product_tag_crud.read_list_tags_by_product(product.id)

            if product.category_id:
                category = await self.category_crud.read_sub_with_parent_by_id(
                    product.category_id
                )
            if product.series_id:
                series = await self.series_crud.get_by_id(product.series_id)
                series.__dict__.pop("created_at")
                series.__dict__.pop("updated_at")
                series.__dict__.pop("deleted_at")
                if series is not None and series.image is not None:
                    series.image = helper.convert_image_to_url(series.image)

            images = await self.products_image_crud.get_list_image_urls(id)
            images = [get_image_from_url(image) for image in images]

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
            logging.warning(e)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Failed to get product {e}",
            )

    async def create_product(self, body: BodyCreateProduct):
        try:
            slug = helper.slugify(body.name)
            type = body.thumbnail_type

            await self.__check_product_exist(slug)

            url = f"products/{slug}.{type}"
            new_product = ProductCreateCRUD(thumbnail=url, **body.model_dump())

            series_id = await self.series_crud.get_by_id(body.series_id)
            category_id = await self.category_crud.read_by_id(body.category_id)
            old_product = await self.product_crud.read_by_slug(body.slug)

            # Check if product already exist, series, category not exist
            if series_id is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Series not found!")
            if category_id is None:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Category not found!")
            if old_product:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Product already exist"
                )

            new_product.series_id = series_id.id
            category_id = category_id.id
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
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found")

            product_images = (
                await self.products_image_crud.read_product_image_by_product_id(id)
            )
            if len(product_images) > 0:
                await self.delete_product_image(id)

            await self.product_crud.delete_by_id(id)
            self.__delete_image_S3(product.thumbnail)

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

    async def create_product_images(self, id: UUID, images: list[ImageType]):
        try:
            is_valid_product = await self.product_crud.read_by_id(id)
            if not is_valid_product:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
            slug = await self.product_crud.read_product_slug(id)

            exist_images_quantity = await self.products_image_crud.read_images_quantity(
                id
            )

            if exist_images_quantity is None:
                exist_images_quantity = 0

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
                "presigned_urls": presigned_urls,
            }
        except Exception as e:
            HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to create product images : {e}"
            )

    async def delete_product_image(self, id: UUID):
        try:
            is_valid_product = await self.product_crud.read_by_id(id)
            if not is_valid_product:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")
            product_images = (
                await self.products_image_crud.read_product_image_by_product_id(id)
            )

            if len(product_images) == 0:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Product Image not found!"
                )

            await self.products_image_crud.delete_by_product_id(id)
            [self.__delete_image_S3(image.image_url) for image in product_images]
            return {"detail": "Product Image deleted successfully"}
        except Exception as e:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to delete product images : {e}"
            )

    async def update_product_image(self, id: UUID, slug: str, body: ImageType):
        try:
            is_valid_product = await self.product_crud.read_by_id(id)
            if not is_valid_product:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product not found!")

            is_valid_id = (
                await self.products_image_crud.read_product_image_by_product_id(id)
            )
            if not is_valid_id:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST, "Product Image slug not found!"
                )

            slug = await self.product_crud.read_product_slug(id) or ""

            image_slug = f"{slug}-{body.order.value}"
            image_url = f"products/{image_slug}.{body.type}"
            for product_image in is_valid_id:
                if product_image.slug == slug:
                    await self.products_image_crud.update(
                        product_image.id, image_slug, image_url
                    )
                    data = self.__create_presigned_url(
                        "customafk-ecommerce-web", image_slug, body.type
                    )
                    if data is None:
                        raise HTTPException(
                            status.HTTP_400_BAD_REQUEST,
                            "Failed to create presigned URL",
                        )
                    return {
                        "detail": "Product Image updated successfully",
                        "presigned_url": data,
                    }
        except Exception as e:
            HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Failed to update product images : {e}"
            )

    async def check_product_image_creation(self, id: UUID, result: int):
        images = await self.products_image_crud.read_product_images(id)
        if result == 0:
            [self.__delete_image_S3(image.image_url) for image in images]
            await self.products_image_crud.delete_by_product_id(id)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create product images"
            )
        return {
            "detail": {"Product Image created successfully"},
        }

    @staticmethod
    def __check_image_quantity(new_images_quantity: int, exist_images_quatity: int):
        return new_images_quantity > 5 - exist_images_quatity

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
