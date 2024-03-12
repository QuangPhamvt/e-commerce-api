from uuid import UUID
from fastapi import HTTPException, status
from app.database.crud import role_crud
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.helper import helper

class Update:
    @staticmethod
    async def update(id: str, new_role_name: str, db: AsyncSession):
        is_exist_name = await role_crud.get_role_by_name(db=db, role_name=new_role_name)
        if is_exist_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Name has been used!"
            )
        role_id = helper.convert_str_to_UUID(id)       
        is_valid_id = await role_crud.get_role_by_id(id=role_id, db=db)
        if not is_valid_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Id not found!"
            )
     
        await role_crud.update_role_by_id(
            role_id=role_id, 
            new_role_name=new_role_name,
            db=db
        )
        return { "message": "Update role succeed!" }