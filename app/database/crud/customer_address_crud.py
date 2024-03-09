from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import CustomerAddress
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.orm import defer


async def get_user_addresses(db: AsyncSession, user_id: UUID):
    list_users = await db.execute(
        select(CustomerAddress)
        .options(
            defer(CustomerAddress.user_id),
            defer(CustomerAddress.created_at),
            defer(CustomerAddress.updated_at),
        )
        .where(CustomerAddress.user_id == user_id)
    )

    return [row.CustomerAddress for row in list_users.mappings()]
