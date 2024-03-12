from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import category_crud


class GetAll:
    @staticmethod
    async def get_all(current: int, limit: int, db: AsyncSession):
        offset = (current - 1) * limit
        total_items = await category_crud.count_category(db=db) or 0
        total_pages = ceil(total_items / limit)
        list_category = await category_crud.get_all_with_paginate(
            offset=offset, limit=limit, db=db
        )
        return {
            "current_page": current,
            "page_size": len(list_category),
            "total_items": total_items,
            "total_pages": total_pages,
            "category": list_category,
        }
