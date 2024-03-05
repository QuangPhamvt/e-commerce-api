from uuid import UUID
from fastapi import HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.schemas.auth import TokenPayload
from app.utils.helper import helper


class Refresh:
    async def refresh(self, request: Request, response: Response, db: AsyncSession):
        payload = await self.__is_valid_token(request=request, db=db)
        if payload:
            new_access_token = helper.create_access_token(user_data=payload)
            new_refresh_token = helper.create_refresh_token(user_data=payload)
            response.set_cookie("access_token", new_access_token, secure=True)
            response.set_cookie("refresh_token", new_refresh_token, secure=True)
            user_id = payload.id
            await user_crud.update_refresh_token(
                db=db, id=user_id, refresh_token=new_refresh_token
            )
            return {"message": "Refresh Succeed!"}

    @staticmethod
    async def __is_valid_token(request: Request, db: AsyncSession):
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            decode = helper.verify_refresh_token(token=refresh_token)
            user_id = UUID(decode["id"])
            role_id = UUID(decode["role_id"])
            user = await user_crud.get_user_by_id(db=db, id=user_id)
            payload = TokenPayload(id=user_id, role_id=role_id)
            if user and user.refresh_token == refresh_token:
                return payload
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token. Please re-login!",
        )
