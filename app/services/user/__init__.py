from uuid import UUID
from app.configs.constants import PHONE_NUMBER
from app.database.crud import bio_crud, role_crud
from app.database.crud.user_crud import UserCRUD
from app.schemas.bio import CreateBioParam
from app.schemas.user import CreateDemoUserParam, CreateUserParam
from app.utils import helper
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

    
class UserService():
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_crud = UserCRUD(db)
    
    async def create_user(self, user: CreateUserParam):

        await self.__check_user_exist(user.email)

        await self.user_crud.create_user(user)
        return {"detail": "Create user succeed!"}
    
    async def delete_user(self, id: UUID):
        user = await self.user_crud.read_user_by_id(id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
 
        await self.user_crud.delete_user_by_id(id) #Chưa có hàm delete_user
        return {"detail": "Delete user succeed!"}
    
    async def update_user(self, id: UUID, user: CreateUserParam):
        is_valid_id = await self.user_crud.read_user_by_email(user.email)
        if not is_valid_id:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Id not found!",
            )
        await self.user_crud.update_user(id, user) #Chưa có hàm update_user
        return {"detail": "Update user succeed!"}
    
    async def __check_user_exist(self, email: str):
        user = await self.user_crud.read_user_by_email(email)
        if user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists!")
        pass

    async def get_list_users(self):
        list_users = await self.user_crud.read_list_users()
        return list_users
    
    async def get_by_id(self, id: UUID):
        user_detail = await self.user_crud.read_user_by_id(id)
        return user_detail
    

    #Tao demo user
    @staticmethod
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

__all__ = ["UserService"]
