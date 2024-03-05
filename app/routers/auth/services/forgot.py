from datetime import datetime, timedelta, timezone
from dotenv import dotenv_values
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import FORGOT_CODE_EXPIRE
from app.database.crud import user_crud
import string
import random


from app.utils.helper import helper


config = dotenv_values(".env")


class Forgot:
    async def forgot_password(self, email: str, db: AsyncSession):
        exist_user = await user_crud.get_user_by_email(email=email, db=db)
        if not exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found!"
            )
        verify_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        expire = FORGOT_CODE_EXPIRE or 600
        expire_seconds = int(expire)
        expire_time = datetime.now(timezone.utc) + timedelta(seconds=expire_seconds)
        await user_crud.upsert_verify_code(
            id=exist_user.id, verify_code=verify_code, expire=expire_time, db=db
        )
        resend_sender = config["RESEND_SENDER"] or "noreply@localhost"
        helper.forgot_email(send_from=resend_sender, send_to=email, code=verify_code)
        return {"message": "Mail has been sent!"}
