from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .services import AuthService
from app.dependencies import get_db
from app.schemas.auth import UserSignUpParam
from app.utils.helper import helper
from app.configs.constants import AUTH, AUTH_PATH, AUTH_PREFIX

SIGN_UP = AUTH_PATH["SIGN_UP"]
VERIFY = AUTH_PATH["VERIFY"]

router = APIRouter(prefix=AUTH_PREFIX, tags=[AUTH])


@router.post(SIGN_UP)
async def handle_signup(user: UserSignUpParam, db: AsyncSession = Depends(get_db)):
    new_user = await AuthService().sign_up(user=user, db=db)
    return new_user


@router.patch(VERIFY)
async def verify(token: str, db: AsyncSession = Depends(get_db)):
    payload = helper.verify_token(token=token)
    await AuthService().verify(payload=payload, db=db)
