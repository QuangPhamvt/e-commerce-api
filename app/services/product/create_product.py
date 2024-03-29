from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.S3.put_object import put_object
from app.database.crud.product_crud import ProductCRUD

from app.schemas.product import ProductCreateCRUD, BodyCreateProduct
from app.utils.helper import helper


class CreateProduct:
    async def create_product(self, body: BodyCreateProduct, db: AsyncSession):
        slug = helper.slugify(body.name)
        type = body.thumbnail_type

        await self.__check_product_exist(slug, db)

        url = f"products/{slug}.{type}"
        new_product = ProductCreateCRUD(thumbnail=url, **body.model_dump())
        await ProductCRUD(db).create(new_product)

        data = self.__create_presigned_url("customafk-ecommerce-web", slug, type)

        if data is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create presigned URL"
            )
        return {"detail": "Product created successfully", "presigned_url": data}

    @staticmethod
    async def __check_product_exist(slug: str, db: AsyncSession):
        product = await ProductCRUD(db).get_product_by_slug(slug)
        if product:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Product already exists!")
        pass

    @staticmethod
    def __create_presigned_url(bucket_name: str, slug: str, type: str):
        url = f"products/{slug}.{type}"
        return put_object(bucket_name, url, type)
