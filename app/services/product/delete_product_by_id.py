from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.S3.delete_object import delete_object_s3
from app.database.crud.product_crud import ProductCRUD


class DeleteProductById:
    async def delete_by_Id(self, id: UUID, db: AsyncSession):
        product = await ProductCRUD(db).get_product_by_id(id)

        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

        await self.__delete_image_S3(product.image)
        await ProductCRUD(db).delete_by_id(id)
        return {"detail": "Product deleted successfully"}

    @staticmethod
    async def __delete_image_S3(image: str):
        delete_object_s3("customafk-ecommerce-web", image)
        pass
