from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import BodyUpdateProduct
from app.database.crud.product_crud import ProductCRUD


class UpdateProductById:
    async def update_product_by_id(
        self, id: UUID, body: BodyUpdateProduct, db: AsyncSession
    ):
        await ProductCRUD(db).update_by_id(id, body)
        return {"detail": f"Update Product {id} Succeed!"}
