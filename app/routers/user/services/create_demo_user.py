from app.database.crud import bio_crud, role_crud, user_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import CreateDemoUserParam, CreateUserParam
from app.schemas.bio import CreateBioParam
from fastapi import HTTPException, status
from app.utils.helper import helper
from uuid import UUID
from app.configs.constants import PHONE_NUMBER, USERNAME

class CreateDemoUser:
    async def create_demo_user(self, user: CreateDemoUserParam, db: AsyncSession):
        role_id = await self.get_role_id(db=db, role_name=user.role_name)
        await self.check_user_exist(email=user.email, db=db)
        new_user = await self.create_user(    
            email=user.email, 
            password=user.password, 
            role_id=role_id,
            db=db
        )
        new_bio = await self.create_bio(
            user_id=new_user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            db=db
        )
        return {
            "message": "User has been created successfully!",
        }
    
    # Get role
    @staticmethod
    async def get_role_id(db: AsyncSession, role_name: str):
        role_id = await role_crud.get_role_id_by_name(db=db, role_name=role_name)
        if role_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found!"
            )
        return role_id
    
    # Check if demo user already exists
    @staticmethod
    async def check_user_exist(email: str, db: AsyncSession):
        get_user_by_email = user_crud.get_user_by_email
        exist_user = await get_user_by_email(email=email, db=db)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email has been used!"
            )
        pass
    
    # Create new demo user
    @staticmethod
    async def create_user(email: str, password: str, role_id: UUID, db: AsyncSession):
        create_user = user_crud.create_user
        new_user_obj = CreateUserParam(
            email=email, 
            password=password, 
            role_id=role_id
        )
        new_user = await create_user(user=new_user_obj, db=db)
        return new_user
    
    # Create new bio
    @staticmethod
    async def create_bio(user_id: UUID, first_name: str, last_name: str, db: AsyncSession):
        new_bio_param = CreateBioParam(
            user_id=user_id,
            fullname=helper.correct_fullname(first_name=first_name, last_name=last_name),
            username=USERNAME,
            phone_number=PHONE_NUMBER
        )
        new_bio = await bio_crud.create_bio(db=db, user_data=new_bio_param)
        return new_bio
