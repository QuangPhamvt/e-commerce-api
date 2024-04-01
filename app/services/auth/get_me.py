from uuid import UUID
from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.schemas.auth import ResGetMe
from app.utils.helper import helper


class GetMe:
    @staticmethod
    async def get_me(request: Request, db: AsyncSession) -> ResGetMe:
        access_token = request.cookies.get("access_token") or "fake_refresh_token"
        decode = helper.verify_access_token(access_token)
        user_id = UUID(decode["id"])
        user = await user_crud.UserCRUD(db).read_user_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User not found!")
        return ResGetMe(**user.__dict__)
