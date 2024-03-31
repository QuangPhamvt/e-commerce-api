from app.database.crud import bio_crud, role_crud, user_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import CreateDemoUserParam, CreateUserParam
from app.schemas.bio import CreateBioParam
from fastapi import HTTPException, status
from app.utils.helper import helper
from uuid import UUID
from app.configs.constants import PHONE_NUMBER


class CreateDemoUser:
    async def create_demo_user(self, user: CreateDemoUserParam, db: AsyncSession):
        role_id = await self.__get_role_id(db, user.role_name)
        await self.__check_user_exist(email=user.email, db=db)

        new_user = await self.__create_user(
            **user.model_dump(exclude={"role_name", "first_name", "last_name"}),
            role_id=role_id,
            db=db,
        )
        await self.__create_bio(
            **user.model_dump(exclude={"role_name", "password"}),
            user_id=new_user.id,
            db=db,
        )
        return {
            "detail": "User has been created successfully!",
        }

    # Get role
    @staticmethod
    async def __get_role_id(db: AsyncSession, role_name: str):
        role = await role_crud.RoleCRUD(db).get_role_by_name(role_name)
        if role is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Role not found!")
        return role.id

    # Check if demo user already exists
    @staticmethod
    async def __check_user_exist(email: str, db: AsyncSession):
        exist_user = await user_crud.UserCRUD(db).read_user_by_email(email)
        if exist_user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email has been used!")
        pass

    # Create new demo user
    @staticmethod
    async def __create_user(email: str, password: str, role_id: UUID, db: AsyncSession):
        new_user_obj = CreateUserParam(email=email, password=password, role_id=role_id)
        new_user = await user_crud.UserCRUD(db).create_user(new_user_obj)
        return new_user

    # Create new bio
    @staticmethod
    async def __create_bio(
        user_id: UUID, email: str, first_name: str, last_name: str, db: AsyncSession
    ):
        new_bio_param = CreateBioParam(
            user_id=user_id,
            fullname=helper.correct_fullname(first_name, last_name),
            username=email.split("@")[0],
            phone_number=PHONE_NUMBER,
        )
        await bio_crud.BioCRUD(db).create_bio(new_bio_param)
