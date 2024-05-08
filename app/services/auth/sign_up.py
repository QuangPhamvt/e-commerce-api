from uuid import UUID
from dotenv import dotenv_values
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import DEFAULT_ROLE_NAME
from app.database.crud import bio_crud, role_crud, user_crud
from app.schemas.bio import CreateBioParam
from app.utils.helper import helper
from app.schemas.auth import UserSignUpParam
from app.schemas.user import CreateUserParam

config = dotenv_values(".env")


class SignUp:
    async def sign_up(self, user: UserSignUpParam, db: AsyncSession) -> dict[str, str]:
        RESEND_SENDER = self.__get_resend_sender()
        email = user.email
        password = user.password
        fullname = user.fullname
        await self.__check_user_exist(email=user.email, db=db)

        user_role = await self.__get_default_role(db=db)

        new_user = await self.__create_user(email, password, user_role.id, db)

        username = new_user.email.split("@")[0]

        helper.verify_email(
            send_from=RESEND_SENDER,
            send_to=new_user.email,
            token=helper.create_verify_token(str(new_user.id)),
        )

        await self.__create_bio(new_user.id, username, fullname, db)

        return {
            "detail": "User has been created successfully!",
        }
    
    async def sign_up_instant_active(self, user: UserSignUpParam, db: AsyncSession):
        email = user.email
        password = user.password
        fullname = user.fullname
        await self.__check_user_exist(email=user.email, db=db)

        user_role = await self.__get_default_role(db=db)

        new_user = await self.__create_user(email, password, user_role.id, db)

        username = new_user.email.split("@")[0]

        await self.__create_bio(new_user.id, username, fullname, db)

        await user_crud.UserCRUD(db).update_verify_with_email(email)
        
        return {
            "detail": "User has been created successfully!",
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
        exist_user = await user_crud.UserCRUD(db).read_user_by_email(email)
        if exist_user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email has been used!")
        pass

    # Get default role
    @staticmethod
    async def __get_default_role(db: AsyncSession):
        user_role = await role_crud.RoleCRUD(db).get_role_by_name(DEFAULT_ROLE_NAME)
        if user_role is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Role not found!")
        return user_role

    # Create new user
    @staticmethod
    async def __create_user(email: str, password: str, role_id: UUID, db: AsyncSession):
        new_user_obj = CreateUserParam(email=email, password=password, role_id=role_id)
        new_user = await user_crud.UserCRUD(db).create_user(new_user_obj)
        return new_user

    # Create new bio
    @staticmethod
    async def __create_bio(
        user_id: UUID, username: str, fullname: str, db: AsyncSession
    ):
        new_bio_param = CreateBioParam(
            user_id=user_id,
            fullname=fullname,
            username=username,
            phone_number="",
        )
        await bio_crud.BioCRUD(db).create_bio(new_bio_param)
