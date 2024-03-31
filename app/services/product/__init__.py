from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.Clounfront import get_image_from_url
from app.configs.S3.delete_object import delete_object_s3
from app.configs.S3.put_object import put_object
from app.database.crud.category_crud import CategoryCRUD
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

            product.__dict__.pop("category_id")
            product.thumbnail = self.__convert_image_to_url(product)
            new_product = {
                "tags": tags,
                "category": category if category else None,
                **product.__dict__,
            }
            return new_product
        except Exception:
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

    @staticmethod
    def __create_presigned_url(bucket_name: str, slug: str, type: str):
        url = f"products/{slug}.{type}"
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
