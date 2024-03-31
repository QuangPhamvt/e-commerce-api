from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.utils.helper import helper


class Verify:
    @staticmethod
    async def verify(payload: str, db: AsyncSession):
        # convert payload to UUID
        user_id = helper.convert_str_to_UUID(id=payload)
        user = await user_crud.UserCRUD(db).read_user_by_id(user_id)
        if user and user.is_active:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "User has been verified!",
            )
        await user_crud.UserCRUD(db).update_verify(user_id)
        return
