import logging
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer
from sqlalchemy import delete, select, update
from app.database.crud.product_crud import ProductCRUD
from app.database.models.Product import Category, Product
from app.schemas.category import (
    CreateCategoryParam,
    UpdateCategoryData,
)
from app.utils.uuid import generate_uuid
from app.utils.helper import helper


class CategoryCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.product_crud = ProductCRUD(db)

    async def create(self, data: CreateCategoryParam):
        try:
            id = generate_uuid()
            slug = helper.slugify(data.name)
            category = Category(
                id=id,
                slug=slug,
                **data.model_dump(),
            )
            self.db.add(category)
            await self.db.commit()
        except Exception as e:
            logging.warning(f"Error creating category : {e}")
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Failed to create category"
            )

    async def is_exist(self, name: str):
        return (
            (
                await self.db.execute(
                    select(Category.id)
                    .where(Category.name == name)
                    .where(Category.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def read_by_id(self, id: UUID):
        return (
            (
                await self.db.execute(
                    select(Category)
                    .options(
                        defer(Category.created_at),
                        defer(Category.updated_at),
                        defer(Category.deleted_at),
                    )
                    .where(Category.id == id)
                    .where(Category.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def read_sub_with_parent_by_id(self, sub_id: UUID):
        sub_category = (
            (
                await self.db.execute(
                    select(Category)
                    .options(
                        defer(Category.created_at),
                        defer(Category.updated_at),
                        defer(Category.deleted_at),
                    )
                    .where(Category.id == sub_id)
                )
            )
            .scalars()
            .first()
        )
        if sub_category is None:
            return None
        parent_category = (
            (
                await self.db.execute(
                    select(Category)
                    .options(
                        defer(Category.parent_id),
                        defer(Category.created_at),
                        defer(Category.updated_at),
                        defer(Category.deleted_at),
                    )
                    .where(Category.id == sub_category.parent_id)
                )
            )
            .scalars()
            .first()
        )
        sub_category.__dict__.pop("parent_id")
        category = {
            **parent_category.__dict__,
            "sub": sub_category,
        }
        return category

    async def read_by_id_and_parent_id(self, id: UUID, parent_id: UUID):
        return (
            (
                await self.db.execute(
                    select(Category)
                    .where(Category.id == id)
                    .where(Category.parent_id == parent_id)
                    .where(Category.deleted_at.is_(None))
                )
            )
            .scalars()
            .first()
        )

    async def delete_sub_by_id(self, sub_id: UUID):
        await self.db.execute(delete(Category).where(Category.id == sub_id))
        await self.db.commit()

    async def delete_parent_by_id(self, id: UUID):
        await self.db.execute(
            update(Product).where(Product.category_id == id).values(category_id=None)
        )
        await self.db.execute(delete(Category).where(Category.id.__eq__(id)))
        await self.db.execute(
            update(Category).where(Category.parent_id == id).values(parent_id=None)
        )
        await self.db.commit()

    async def update(self, id: UUID, data: UpdateCategoryData):
        slug = helper.slugify(data.name)
        await self.db.execute(
            update(Category)
            .where(Category.id == id)
            .values(
                **data.model_dump(),
                slug=slug,
            )
        )
        await self.db.commit()

    async def update_parent_id_for_subcategory(
        self, parent_id: UUID, list_sub_id: list[UUID]
    ):
        await self.db.execute(
            update(Category)
            .where(Category.id.in_(list_sub_id))
            .values(parent_id=parent_id)
        )
        await self.db.commit()

    async def read_all(self):
        list_category = await self.db.execute(
            select(Category)
            .options(
                defer(Category.parent_id),
                defer(Category.created_at),
                defer(Category.updated_at),
            )
            .where(Category.parent_id.is_(None))
        )
        results = [
            {
                **category.Category.asdict(),
                "sub": await self.read_sub_category(category.Category.id),
            }
            for category in list_category.mappings()
        ]
        return results

    async def read_list_id(self):
        return (
            (
                await self.db.execute(
                    select(Category.id).where(Category.parent_id.is_(None))
                )
            )
            .scalars()
            .all()
        )

    async def read_sub_category(self, parent_id: UUID):
        return (
            (
                await self.db.execute(
                    select(Category)
                    .options(
                        defer(Category.parent_id),
                        defer(Category.created_at),
                        defer(Category.updated_at),
                        defer(Category.deleted_at),
                    )
                    .where(Category.parent_id == parent_id)
                )
            )
            .scalars()
            .all()
        )

    async def update_product(self, product_id: UUID, category_id: UUID):
        await self.db.execute(
            update(Product)
            .where(Product.id == product_id)
            .values(category_id=category_id)
        )
        await self.db.commit()
