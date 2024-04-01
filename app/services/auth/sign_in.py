from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.database.models import User
from app.schemas.auth import TokenPayload, UserSignInParam
from app.utils.helper import helper
from fastapi import Response
from dotenv import dotenv_values


config = dotenv_values(".env")


class SignIn:
    async def sign_in(
        self, user: UserSignInParam, response: Response, db: AsyncSession
    ):
        email = user.email
        password = user.password
        user_data = await self.__authenticate_user(email, password, db)
        if not user_data:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Incorrect Email or Password",
            )
        if not user_data.is_active:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User is not active")
        payload = TokenPayload(id=user_data.id, role_id=user_data.role_id)
        await self.__gen_token(payload, response, user_data, db)

    @staticmethod
    async def __authenticate_user(
        email: str, password: str, db: AsyncSession
    ) -> User | None:
        user = await user_crud.get_user_by_email(email, db)
        if not user:
            return None

        user_hash_password = str(user.hash_password)
        is_correct_password = helper.verify_password(password, user_hash_password)
        if not is_correct_password:
            return None

        return user

    @staticmethod
    async def __gen_token(
        payload: TokenPayload, response: Response, user_data: User, db: AsyncSession
    ):
        update_refresh_token = user_crud.update_refresh_token
        at_seconds = 600
        rt_seconds = 604800
        if config["ACCESS_TOKEN_EXPIRE"]:
            at_seconds = int(config["ACCESS_TOKEN_EXPIRE"])
        if config["REFRESH_TOKEN_EXPIRE"]:
            rt_seconds = int(config["REFRESH_TOKEN_EXPIRE"])

        access_token = helper.create_access_token(payload)
        refresh_token = helper.create_refresh_token(payload)
        response.set_cookie(
            "access_token",
            access_token,
            at_seconds,
            secure=True,
            httponly=True,
            domain="customafk.com",
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            rt_seconds,
            secure=True,
            httponly=True,
            domain="customafk.com",
        )
        await update_refresh_token(user_data.id, refresh_token, db)
