from typing import Sequence
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Product
from app.utils.helper import helper
from app.utils.uuid import generate_uuid
from app.schemas.product import BodyUpdateProduct, ProductCreateCRUD


class ProductCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product: ProductCreateCRUD) -> None:
        db = self.db
        uuid = generate_uuid()
        slug = helper.slugify(product.name)
        db_proudct = Product(
            id=uuid,
            slug=str(slug),
            category_id=None,
            **product.model_dump(),
        )
        db.add(db_proudct)
        await db.commit()
        await db.refresh(db_proudct)
        return

    async def get_product_by_id(self, id: UUID) -> Product | None:
        db = self.db
        product = await db.execute(select(Product).where(Product.id == id))
        return product.scalars().first()

    async def get_product_by_slug(self, slug: str) -> Product | None:
        db = self.db
        product = await db.execute(select(Product).where(Product.slug == slug))
        return product.scalars().first()

    async def get_products(self) -> Sequence[Product]:
        db = self.db
        products = await db.execute(select(Product))
        return products.scalars().all()

    async def delete_by_id(self, id: UUID) -> None:
        db = self.db
        await db.execute(delete(Product).where(Product.id == id))
        await db.commit()
        pass

    async def update_by_id(self, id: UUID, product: BodyUpdateProduct) -> None:
        db = self.db
        data = {k: v for k, v in product.dict().items() if v is not None}
        await db.execute(update(Product).where(Product.id == id).values(data))
        await db.commit()
        pass
