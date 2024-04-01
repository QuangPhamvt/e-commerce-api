from uuid import UUID
from fastapi import HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.schemas.auth import TokenPayload
from app.utils.helper import helper
from dotenv import dotenv_values

config = dotenv_values(".env")


class Refresh:
    async def refresh(self, request: Request, response: Response, db: AsyncSession):
        payload = await self.__is_valid_token(request=request, db=db)
        if payload:
            at_seconds = 600
            rt_seconds = 604800

            if config["ACCESS_TOKEN_EXPIRE"]:
                at_seconds = int(config["ACCESS_TOKEN_EXPIRE"])
            if config["REFRESH_TOKEN_EXPIRE"]:
                rt_seconds = int(config["REFRESH_TOKEN_EXPIRE"])
            new_access_token = helper.create_access_token(user=payload)
            new_refresh_token = helper.create_refresh_token(user=payload)

            response.set_cookie(
                "access_token",
                new_access_token,
                at_seconds,
                secure=True,
                httponly=True,
                domain="customafk.com",
            )
            response.set_cookie(
                "refresh_token",
                new_refresh_token,
                rt_seconds,
                secure=True,
                httponly=True,
                domain="customafk.com",
            )
            user_id = payload.id
            await user_crud.update_refresh_token(
                db=db, id=user_id, refresh_token=new_refresh_token
            )
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Invalid refresh token. Please re-login!",
            )

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
            status.HTTP_400_BAD_REQUEST,
            "Invalid refresh token. Please re-login!",
        )
