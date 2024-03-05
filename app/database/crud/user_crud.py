from datetime import datetime
from uuid import UUID
from sqlalchemy import select, update
from app.database.models import User
from app.database.models.User import ResetPassword
from app.schemas.auth import VerifyPayload
from app.schemas.user import CreateUserParam
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper
from app.utils.uuid import generate_uuid


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


async def verify_user(db: AsyncSession, payload: VerifyPayload):
    user_id = payload.user_id
    print(f"From CRUD: user_id: {user_id}, type: {type(user_id)}")
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
