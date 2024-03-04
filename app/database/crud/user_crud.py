from sqlalchemy import select, update
from app.database.models import User
from app.schemas.auth import UserSignUpParam, VerifyPayload
from app.schemas.user import CreateUserParam
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper
from app.utils.uuid import generate_uuid


async def get_user_by_email(
    user: UserSignUpParam,
    db: AsyncSession,
) -> User | None:
    data_user = await db.execute(select(User).where(User.email == user.email))
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
