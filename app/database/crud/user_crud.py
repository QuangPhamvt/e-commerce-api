from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import defer
from sqlalchemy import select, update
from app.database.models import User, Bio, CustomerAddress, Role
from app.database.models.User import ResetPassword
from app.schemas.user import CreateUserParam
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper
from app.utils.uuid import generate_uuid
from app.database.crud import customer_address_crud


async def get_user_by_email(
    email: str,
    db: AsyncSession,
) -> User | None:
    data_user = await db.execute(select(User).where(User.email == email))
    return data_user.scalars().first()


async def create_user(user: CreateUserParam, db: AsyncSession) -> User:
    user_id = generate_uuid()
    hash_password = helper.hash_password(password=user.password)
    db_user = User(
        id=user_id,
        email=user.email,
        hash_password=hash_password,
        role_id=user.role_id,
        is_active=False,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def verify_user(db: AsyncSession, user_id: UUID):
    await db.execute(update(User).where(User.id == user_id).values(is_active=True))
    await db.commit()


async def update_refresh_token(id: UUID, refresh_token: str, db: AsyncSession):
    await db.execute(
        update(User).where(User.id == id).values(refresh_token=refresh_token)
    )
    await db.commit()


async def get_user_by_id(id: UUID, db: AsyncSession):
    data_user = await db.execute(select(User).where(User.id == id))
    return data_user.scalars().first()


async def upsert_verify_code(
    id: UUID, verify_code: str, expire: datetime, db: AsyncSession
):
    data_user = await db.execute(
        select(ResetPassword).where(ResetPassword.user_id == id)
    )

    user_reset = data_user.scalars().first()
    if not user_reset:
        db_user_reset = ResetPassword(user_id=id, code=verify_code, expire_at=expire)
        db.add(db_user_reset)
        await db.commit()
    else:
        await db.execute(
            update(ResetPassword)
            .where(ResetPassword.user_id == id)
            .values(code=verify_code, expire_at=expire)
        )
        await db.commit()


async def get_user_reset_password(id: UUID, db: AsyncSession):
    user_reset_password = await db.execute(
        select(ResetPassword).where(ResetPassword.user_id == id)
    )
    return user_reset_password.scalars().first()


async def reset_password(id: UUID, hash_password: bytes, db: AsyncSession):
    await db.execute(
        update(User).where(User.id == id).values(hash_password=hash_password)
    )
    await db.commit()

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