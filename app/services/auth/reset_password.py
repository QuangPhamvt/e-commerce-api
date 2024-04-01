from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.utils.helper import helper


class ResetPassword:
    @staticmethod
    async def reset_password(
        email: str, verify_code: str, new_password: str, db: AsyncSession
    ):
        exist_user = await user_crud.UserCRUD(db).read_user_by_email(email)
        if not exist_user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email not found!")
        user_reset_password = await user_crud.UserCRUD(db).read_user_reset_password(
            exist_user.id
        )
        if user_reset_password:
            now = datetime.today()
            expire_time = user_reset_password.expire_at
            is_valid_code = (
                user_reset_password.code == verify_code and expire_time > now
            )
            if is_valid_code:
                hash_password = helper.hash_password(password=new_password)
                await user_crud.UserCRUD(db).update_password(
                    exist_user.id, hash_password
                )
                return {"detail": "Reset Password Succeed!"}
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Incorrect Verification Code! Maybe it's wrong or be expired",
        )
