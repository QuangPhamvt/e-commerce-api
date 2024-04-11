from lib2to3.pytree import convert
import logging
from uuid import UUID
from app.configs.constants import PHONE_NUMBER
from app.database.crud import  role_crud
from app.database.crud.user_crud import UserCRUD
from app.schemas.user import CreateUserParam
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.utils.helper import helper
from app.utils.uuid import convert_str_to_uuid


    
class UserService():
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_crud = UserCRUD(db)
    
    async def create(self, body: CreateUserParam):
        try:
            user = await self.user_crud.read_user_by_email(body.email)
            if user:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    "User exist!",
                )
            await self.user_crud.create_user(body)
        except Exception as e:
            logging.warning(e)
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Failed to create user {e}",
            )
        return {"detail": "Create user succeed!"}
    
    async def delete_user(self, id: UUID):
        user = await self.user_crud.read_user_by_id(id)

        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
 
        await self.user_crud.delete_user_by_id(id) 
        return {"detail": "Delete user succeed!"}
    
    async def update_user(self, id: str, password: str):
        try:
            converted_id = convert_str_to_uuid(id)
            hash_password = helper.hash_password(password = password)
            await self.user_crud.update_password(converted_id, hash_password) 
            return {"detail": "Update user succeed!"}
        except Exception as e:
            logging.warning(e)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to update user")

    
    async def get_all(self):
        user_list = await self.user_crud.get_all()
        return user_list


    async def get_by_id(self, id: UUID):
        user_detail = await self.user_crud.read_user_by_id(id)
        return user_detail
    
    async def _get_role_id(self, db: AsyncSession, role_name: str):
        role = await role_crud.RoleCRUD(db).get_role_by_name(role_name)
        if role is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Role not found!")
        return role.id
    
    async def __check_user_exist(self, email: str):
        user = await self.user_crud.read_user_by_email(email)
        if user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists!")
        pass

__all__ = ["UserService"]
