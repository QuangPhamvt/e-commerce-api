from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from app.database.models import Product
from app.database.models.Product import product_tag

async def create(product_id: UUID, tag_id: UUID, db: AsyncSession):
    await db.execute(product_tag.insert().values(product_id=product_id, tag_id=tag_id))
    await db.commit()


async def is_exist_product_tag(product_id: UUID, tag_id: UUID, db: AsyncSession):
    result = await db.execute(
        product_tag.select()
        .where(product_tag.c.product_id == product_id)
        .where(product_tag.c.tag_id == tag_id)
    )
    return result.scalars().first()


async def get_list_products_by_tag(tag_id: UUID, db: AsyncSession):
    result = await db.execute(
        product_tag.select()
        .options(
            defer(Product.created_at),
            defer(Product.updated_at),
            defer(product_tag.c.product_id),
        )
        .join(Product, product_tag.c.product_id == Product.id)
        .where(product_tag.c.tag_id == tag_id)
    )
    return result.scalars().all()
