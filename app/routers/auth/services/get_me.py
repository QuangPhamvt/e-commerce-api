from uuid import UUID
from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.utils.helper import helper


class GetMe:
    @staticmethod
    async def get_me(request: Request, db: AsyncSession):
        access_token = request.cookies.get("access_token") or "fake_refresh_token"
        decode = helper.verify_access_token(token=access_token)
        user_id = UUID(decode["id"])
        user = await user_crud.get_user_by_id(db=db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found!"
            )
        user_data = {
            "id": user.id,
            "role_id": user.role_id,
            "email": user.email,
            "is_active": user.is_active,
        }
        return user_data
