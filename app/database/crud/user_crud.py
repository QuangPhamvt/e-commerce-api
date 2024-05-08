from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import defer
from sqlalchemy import select, update
from app.database.models import User, Bio, Role
from app.database.models.User import ResetPassword
from app.schemas.user import CreateUserParam
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper
from app.utils.uuid import generate_uuid
from app.database.crud import customer_address_crud


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def read_user_by_email(self, email: str) -> User | None:
        data_user = await self.db.execute(select(User).where(User.email == email))
        return data_user.scalars().first()
    
    async def get_password_by_email(self, email: str) -> User | None:
        data_user = await self.db.execute(select(User.hash_password).where(User.email == email))
        return data_user.scalars().first()
    
    async def create_user(self, user: CreateUserParam) -> User:
        user_id = generate_uuid()
        hash_password = helper.hash_password(password=user.password)
        db_user = User(
            id=user_id,
            email=user.email,
            hash_password=hash_password,
            role_id=user.role_id,
            is_active=False,
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_verify_with_email(self, email: str):
        await self.db.execute(
            update(User).where(User.email == email).values(is_active=True)
        )
        await self.db.commit()
        
    async def update_verify(self, user_id: UUID):
        await self.db.execute(
            update(User).where(User.id == user_id).values(is_active=True)
        )
        await self.db.commit()

    async def update_refresh_token(self, id: UUID, refresh_token: str | None):
        await self.db.execute(
            update(User).where(User.id == id).values(refresh_token=refresh_token)
        )
        await self.db.commit()

    async def read_user_by_id(self, id: UUID):
        data_user = await self.db.execute(select(User).where(User.id == id))
        return data_user.scalars().first()

    async def update_verify_code(self, id: UUID, verify_code: str, expire: datetime):
        data_user = await self.db.execute(
            select(ResetPassword).where(ResetPassword.user_id == id)
        )

        user_reset = data_user.scalars().first()
        if not user_reset:
            db_user_reset = ResetPassword(
                user_id=id, code=verify_code, expire_at=expire
            )
            self.db.add(db_user_reset)
            await self.db.commit()
        else:
            await self.db.execute(
                update(ResetPassword)
                .where(ResetPassword.user_id == id)
                .values(code=verify_code, expire_at=expire)
            )
            await self.db.commit()

    async def read_user_reset_password(self, id: UUID):
        user_reset_password = await self.db.execute(
            select(ResetPassword).where(ResetPassword.user_id == id)
        )
        return user_reset_password.scalars().first()


    async def update_password(self, id: UUID, hash_password: bytes):
        await self.db.execute(
            update(User).where(User.id == id).values(hash_password=hash_password)
        )
        await self.db.commit()

    async def read_list_users(self):
        list_users = await self.db.execute(
            select(User, Bio, Role.name)
            .options(
                defer(User.hash_password),
                defer(User.refresh_token),
                defer(Bio.user_id),
                defer(Bio.created_at),
            )
            .join(Bio, Bio.user_id == User.id)
            .join(Role, Role.id == User.role_id)
        )

        results = [
            {
                **data_user.User.asdict(),
                **data_user.Bio.asdict(),
                "role": data_user.name,
                "addresses": await customer_address_crud.get_user_addresses(
                    db=self.db, user_id=data_user.User.id
                ),
            }
            for data_user in list_users.mappings()
        ]

        return results
