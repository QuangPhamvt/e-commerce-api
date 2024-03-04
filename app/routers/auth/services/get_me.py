from uuid import UUID
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.schemas.user import UserResponse

from app.utils.helper import helper


class GetMe:
    @staticmethod
    async def get_me(request: Request, db: AsyncSession):
        refresh_token = request.cookies.get("refresh_token")
        decode = helper.verify_refresh_token(token=refresh_token)
        user_id = UUID(decode["id"])
        user: UserResponse = await user_crud.get_user_by_id(db=db, id=user_id)
        user_data = {
            "id": user.id,
            "role_id": user.role_id,
            "email": user.email,
            "is_active": user.is_active,
        }
        return user_data
