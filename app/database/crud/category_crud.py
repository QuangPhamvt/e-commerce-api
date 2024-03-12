from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.sql.expression import func
from app.database.models.Product import Category
from app.schemas.category import CreateCategoryParam, UpdateCategoryParam
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from app.utils.uuid import generate_uuid


async def create_category(
    category: CreateCategoryParam, parent_id: UUID | None, db: AsyncSession
):
    id = generate_uuid()
    db_category = Category(
        id=id,
        name=category.name,
        description=category.description,
        slug=category.slug,
        parent_id=parent_id,
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def is_exist_name(name: str, db: AsyncSession):
    category = await db.execute(select(Category).where(Category.name == name))
    return category.scalars().first()


async def get_category_by_id(id: UUID, db: AsyncSession):
    category = await db.execute(select(Category).where(Category.id == id))
    return category.scalars().first()


async def get_category_by_id_and_parent_id(id: UUID, parent_id: UUID, db: AsyncSession):
    category = await db.execute(
        select(Category).where(Category.id == id).where(Category.parent_id == parent_id)
    )
    return category.scalars().first()


async def delete_sub_category_by_parent_id(parent_id: UUID, db: AsyncSession):
    await db.execute(delete(Category).where(Category.parent_id == parent_id))
    await db.commit()


async def delete_category(id: UUID, db: AsyncSession):
    await db.execute(delete(Category).where(Category.id == id))
    await db.commit()


async def update_category(id: UUID, category: UpdateCategoryParam, db: AsyncSession):
    await db.execute(
        update(Category)
        .where(Category.id == id)
        .values(
            {
                "name": category.name,
                "description": category.description,
                "slug": category.slug,
            }
        )
    )
    await db.commit()


async def count_category(db: AsyncSession):
    none_id = None
    count = await db.execute(
        select(func.count(Category.id))
        .where(Category.parent_id == none_id)
        .order_by(None)
    )
    return count.scalar()


async def get_all_with_paginate(offset: int, limit: int, db: AsyncSession):
    none_id = None
    list_category = await db.execute(
        select(Category)
        .options(
            defer(Category.parent_id),
            defer(Category.created_at),
            defer(Category.updated_at),
        )
        .where(Category.parent_id == none_id)
        .offset(offset=offset)
        .limit(limit=limit)
    )
    results = [
        {
            **category.Category.asdict(),
            "sub": await get_sub_category(parent_id=category.Category.id, db=db),
        }
        for category in list_category.mappings()
    ]
    return results


async def get_sub_category(parent_id: UUID, db: AsyncSession):
    list_sub_category = await db.execute(
        select(Category)
        .options(
            defer(Category.parent_id),
            defer(Category.created_at),
            defer(Category.updated_at),
        )
        .where(Category.parent_id == parent_id)
    )
    return list_sub_category.scalars().all()
