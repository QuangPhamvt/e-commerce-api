from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import DEFAULT_ROLE_NAME
from app.database.crud import role_crud, user_crud
from app.schemas.auth import UserSignUpParam, VerifyPayload
from app.schemas.user import CreateUserParam, UserResponse


class AuthService:
    @staticmethod
    async def sign_up(user: UserSignUpParam, db: AsyncSession) -> UserResponse:
        exist_user = await user_crud.get_user_by_email(db=db, user=user)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email has been used!"
            )
        user_role = await role_crud.get_role_by_name(db=db, role_name=DEFAULT_ROLE_NAME)
        new_user_obj = CreateUserParam(
            email=user.email, password=user.password, role_id=user_role.id
        )
        return await user_crud.create_user(db=db, user=new_user_obj)

    @staticmethod
    async def verify(payload: VerifyPayload, db: AsyncSession):
        print(f"from service: ${payload}")
        await user_crud.verify_user(db=db, payload=payload)


auth_service: AuthService = AuthService()
