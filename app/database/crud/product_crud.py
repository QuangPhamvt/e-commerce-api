from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Product
from app.utils.uuid import generate_uuid
from app.schemas.product import ProductCreate


class ProductCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product: ProductCreate):
        db = self.db
        uuid = generate_uuid()
        db_proudct = Product(
            id=uuid,
            name=product.name,
            slug="",
            description=product.description,
            original_price=product.original_price,
            sell_price=product.sell_price,
            quantity=product.quantity,
            image="",
            country=product.country,
            factory=product.factory,
            status=product.status,
            category_id=None,
        )
        db.add(db_proudct)
        await db.commit()
        await db.refresh(db_proudct)
        return "success"
