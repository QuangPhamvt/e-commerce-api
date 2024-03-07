from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Bio, User, CustomerAddress, Role
from sqlalchemy import select, label
from sqlalchemy.orm import defer
from app.database.crud import customer_address_crud

async def get_list_users(db: AsyncSession):
    list_users = await db.execute(
        select(User, Bio, Role.name)
        .options(
            defer(User.hash_password), 
            defer(User.refresh_token), 
            defer(Bio.user_id), 
            defer(Bio.created_at))
        .join(Bio, Bio.user_id == User.id)
        .join(Role, Role.id == User.role_id))
    
    results = [
        {
            **data_user.User.asdict(),
            **data_user.Bio.asdict(),
            'role': data_user.name,
            'adresses': await customer_address_crud.get_user_addresses(db = db, user_id = data_user.User.id)
        } for data_user in list_users.mappings()
    ]

    return results