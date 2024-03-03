from sqlalchemy import select, update
from app.database import models
from app.schemas.auth import VerifyPayload
from app.schemas.user import CreateUserParam, GetUserByEmailParam, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper
import uuid
from app.utils.uuid import generate_uuid


async def get_user_by_email(
    db: AsyncSession, user: GetUserByEmailParam
) -> UserResponse | None:
    data_user = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    return data_user.scalars().first()


async def create_user(db: AsyncSession, user: CreateUserParam) -> UserResponse:
    user_id = generate_uuid()
    hash_password = helper.hash_password(password=user.password)
    db_user = models.User(
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
    user_id = uuid.UUID(payload["user_id"])
    print(f"From CRUD: user_id: {user_id}, type: {type(user_id)}")
    await db.execute(
        update(models.User).where(models.User.id == user_id).values(is_active=True)
    )

    await db.commit()
