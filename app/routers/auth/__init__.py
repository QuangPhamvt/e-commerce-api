from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from .services import AuthService
from app.dependencies import get_db
from app.schemas.auth import UserSignInParam, UserSignUpParam
from app.utils.helper import helper
from app.configs.constants import AUTH, AUTH_PATH, AUTH_PREFIX

SIGN_UP = AUTH_PATH["SIGN_UP"]
VERIFY = AUTH_PATH["VERIFY"]
SIGN_IN = AUTH_PATH["SIGN_IN"]
LOG_OUT = AUTH_PATH["LOG_OUT"]
REFRESH = AUTH_PATH["REFRESH"]
GET_ME = AUTH_PATH["GET_ME"]

router = APIRouter(prefix=AUTH_PREFIX, tags=[AUTH])


@router.post(SIGN_UP)
async def signup(user: UserSignUpParam, db: AsyncSession = Depends(get_db)):
    new_user = await AuthService().sign_up(user=user, db=db)
    return new_user


@router.patch(VERIFY)
async def verify(token: str, db: AsyncSession = Depends(get_db)):
    payload = helper.verify_token(token=token)
    await AuthService().verify(payload=payload, db=db)


@router.post(SIGN_IN)
async def sign_in(
    user: UserSignInParam, response: Response, db: AsyncSession = Depends(get_db)
):
    return await AuthService().sign_in(user=user, response=response, db=db)


@router.delete(LOG_OUT)
async def logout(db: AsyncSession = Depends(get_db)):
    pass


@router.get(REFRESH)
async def refresh(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    return await AuthService().refresh(request=request, response=response, db=db)


@router.get(GET_ME)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    return await AuthService.get_me(request=request, db=db)
