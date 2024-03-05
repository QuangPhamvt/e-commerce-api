from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.database.models import User
from app.schemas.auth import TokenPayload, UserSignInParam
from app.utils.helper import helper
from fastapi import Response


class SignIn:
    async def sign_in(
        self, user: UserSignInParam, response: Response, db: AsyncSession
    ):
        user_data = await self.__authenticate_user(
            email=user.email, password=user.password, db=db
        )
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Email or Password",
            )
        payload = TokenPayload(id=user_data.id, role_id=user_data.role_id)
        await self.__gen_token(
            payload=payload, response=response, user_data=user_data, db=db
        )

    @staticmethod
    async def __authenticate_user(
        email: str, password: str, db: AsyncSession
    ) -> User | None:
        user = await user_crud.get_user_by_email(email=email, db=db)
        if not user:
            return None
        user_hash_password = str(user.hash_password)
        is_correct_password = helper.verify_password(
            password=password, hash_password=user_hash_password
        )
        if not is_correct_password:
            return None
        return user

    @staticmethod
    async def __gen_token(
        payload: TokenPayload, response: Response, user_data: User, db: AsyncSession
    ):
        update_refresh_token = user_crud.update_refresh_token
        access_token = helper.create_access_token(user=payload)
        refresh_token = helper.create_refresh_token(user=payload)
        response.set_cookie("access_token", access_token, secure=True)
        response.set_cookie("refresh_token", refresh_token, secure=True)
        await update_refresh_token(id=user_data.id, refresh_token=refresh_token, db=db)