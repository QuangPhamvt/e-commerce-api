from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models.Product import Tag, product_tag, Product


async def create(product_id: UUID, tag_id: UUID, db: AsyncSession):
    await db.execute(product_tag.insert().values(product_id=product_id, tag_id=tag_id))
    await db.commit()


async def is_exist_product_tag(product_id: UUID, tag_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(product_tag)
        .where(product_tag.c.product_id == product_id)
        .where(product_tag.c.tag_id == tag_id)
    )
    return result.scalars().first()


async def get_list_products_by_tag(tag_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Product)
        .select_from(product_tag)
        .join(Product, product_tag.c.product_id == Product.id)
        .where(product_tag.c.tag_id == tag_id)
    )
    return result.scalars().all()


async def get_list_tags_by_product(product_id: UUID, db: AsyncSession):
    result = await db.execute(
        select(Tag)
        .select_from(product_tag)
        .join(Tag, product_tag.c.tag_id == Tag.id)
        .where(product_tag.c.product_id == product_id)
        .where(Tag.deleted_at.is_(None))
    )
    return result.scalars().all()
