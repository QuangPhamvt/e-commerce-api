from dotenv import dotenv_values
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import DEFAULT_ROLE_NAME
from app.database.crud import role_crud, user_crud
from app.database.models import User
from app.utils.helper import helper
from app.schemas.auth import UserSignUpParam
from app.schemas.user import CreateUserParam

config = dotenv_values(".env")


class SignUp:
    async def sign_up(self, user: UserSignUpParam, db: AsyncSession) -> User:
        RESEND_SENDER = self.__get_resend_sender()

        get_role_by_name = role_crud.get_role_by_name
        get_user_by_email = user_crud.get_user_by_email
        create_user = user_crud.create_user

        exist_user = await get_user_by_email(email=user.email, db=db)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email has been used!"
            )

        user_role = await get_role_by_name(db=db, role_name=DEFAULT_ROLE_NAME)
        if user_role is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found!"
            )

        new_user_obj = CreateUserParam(
            email=user.email, password=user.password, role_id=user_role.id
        )

        new_user = await create_user(user=new_user_obj, db=db)

        helper.verify_email(
            send_from=RESEND_SENDER,
            send_to="quangpm220503vt@gmail.com",
            token=helper.create_verify_token(user_id=str(new_user.id)),
        )
        return new_user

    @staticmethod
    def __get_resend_sender():
        if config["RESEND_SENDER"] is not None:
            return config["RESEND_SENDER"]
        return "noreply@localhost"
