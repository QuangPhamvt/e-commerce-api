from app.database.crud import bio_crud, role_crud, user_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import CreateDemoUserParam, CreateUserParam
from app.schemas.bio import CreateBioParam
from fastapi import HTTPException, status
from ....utils.helper import helper
from ....configs.constants import PHONE_NUMBER, USERNAME

class CreateDemoUser:
    async def create_user(self, user: CreateDemoUserParam, db: AsyncSession):
        role_id = await self.__get_role_id(db=db, role_name=user.role_name)
        
        new_user_param = CreateUserParam(
            email=user.email, 
            password=user.password, 
            role_id=role_id)

        new_user = await user_crud.create_user(user=new_user_param, db=db)

        new_bio_param = CreateBioParam(
            user_id=new_user.id,
            fullname=helper.correct_fullname(first_name=user.first_name, last_name=user.last_name),
            username=USERNAME,
            phone_number=PHONE_NUMBER
        )

        new_bio = await bio_crud.create_bio(db=db, user_data=new_bio_param)

        return {
            "message": "User has been created successfully!",
        }
    
    # Get role
    @staticmethod
    async def __get_role_id(db: AsyncSession, role_name: str):
        role_id = await role_crud.get_role_id_by_name(db=db, role_name=role_name)
        if role_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role not found!"
            )
        return role_id
