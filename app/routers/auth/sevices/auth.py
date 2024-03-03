from fastapi import APIRouter, Depends

from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import UserSignUpParam
from app.services.auth_service import auth_service
from app.utils.helper import helper
from dotenv import dotenv_values

config = dotenv_values(".env")
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
async def handle_signup(user: UserSignUpParam, db: AsyncSession = Depends(get_db)):
    new_user = await auth_service.sign_up(user=user, db=db)
    helper.verify_email(
        send_from=config["RESEND_SENDER"],
        send_to="qminhqb@gmail.com",
        token=helper.create_verify_token(user_id=str(new_user.id)),
    )
    return new_user


@router.patch("/verify")
async def verify(token: str, db: AsyncSession = Depends(get_db)):
    payload: dict = helper.verify_token(token=token)
    print(f"From Router: {payload}")
    await auth_service.verify(payload=payload, db=db)
