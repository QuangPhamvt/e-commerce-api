from uuid import UUID
from dotenv import dotenv_values
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import DEFAULT_ROLE_NAME
from app.database.crud import role_crud, user_crud
from app.utils.helper import helper
from app.schemas.auth import UserSignUpParam
from app.schemas.user import CreateUserParam

config = dotenv_values(".env")


class SignUp:
    async def sign_up(self, user: UserSignUpParam, db: AsyncSession) -> dict[str, str]:
        RESEND_SENDER = self.__get_resend_sender()

        await self.__check_user_exist(email=user.email, db=db)
        user_role = await self.__get_default_role(db=db)
        new_user = await self.__create_user(
            email=user.email, password=user.password, role_id=user_role.id, db=db
        )

        helper.verify_email(
            send_from=RESEND_SENDER,
            send_to=new_user.email,
            token=helper.create_verify_token(user_id=str(new_user.id)),
        )

        return {
            "message": "User has been created successfully!",
        }

    # Get resend sender
    @staticmethod
    def __get_resend_sender():
        if config["RESEND_SENDER"] is not None:
            return config["RESEND_SENDER"]
        return "noreply@localhost"

    # Check if user already exists
    @staticmethod
    async def __check_user_exist(email: str, db: AsyncSession):
        get_user_by_email = user_crud.get_user_by_email
        exist_user = await get_user_by_email(email=email, db=db)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email has been used!"
            )
        pass

    # Get default role
    @staticmethod
    async def __get_default_role(db: AsyncSession):
        get_role_by_name = role_crud.get_role_by_name
        user_role = await get_role_by_name(db=db, role_name=DEFAULT_ROLE_NAME)
        if user_role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found!"
            )
        return user_role

    # Create new user
    @staticmethod
    async def __create_user(email: str, password: str, role_id: UUID, db: AsyncSession):
        create_user = user_crud.create_user
        new_user_obj = CreateUserParam(email=email, password=password, role_id=role_id)
        new_user = await create_user(user=new_user_obj, db=db)
        return new_user
