from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import dependencies
from app.dependencies import get_db
from app.schemas.auth import ResGetMe, UserSignInParam, UserSignUpParam, VerifyParam
from app.services.auth import AuthService
from app.utils.helper import helper
from app.configs.constants import AUTH, AUTH_PATH, AUTH_PREFIX
from app.schemas.responses import ResBadRequest

SIGN_UP = AUTH_PATH["SIGN_UP"]
VERIFY = AUTH_PATH["VERIFY"]
SIGN_IN = AUTH_PATH["SIGN_IN"]
LOG_OUT = AUTH_PATH["LOG_OUT"]
REFRESH = AUTH_PATH["REFRESH"]
GET_ME = AUTH_PATH["GET_ME"]
FORGOT = AUTH_PATH["FORGOT"]
RESET = AUTH_PATH["RESET"]


router = APIRouter(
    prefix=AUTH_PREFIX,
    tags=[AUTH],
    responses={
        400: {
            "model": ResBadRequest,
            "description": "Description when error occurs",
        },
    },
)


# ********** SIGN UP **********
@router.post(
    SIGN_UP,
    description="This endpoint is used to create a new user.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "User has been created successfully!",
        },
    },
)
async def signup(user: UserSignUpParam, db: AsyncSession = Depends(get_db)):
    res = await AuthService().sign_up(user=user, db=db)
    return res


# ********** VERIFY **********
@router.patch(
    VERIFY,
    description="This endpoint is used to verify user's email.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Verify Succeed!",
        },
    },
)
async def verify(body: VerifyParam, db: AsyncSession = Depends(get_db)):
    token = body.token
    payload = helper.verify_token(token=token)
    await AuthService().verify(payload=payload, db=db)
    return {"message": "Verify Succeed!"}


# ********** SIGN IN **********
@router.post(
    SIGN_IN,
    description="This endpoint is used to sign in.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Sign In Succeed!",
        },
    },
)
async def sign_in(
    user: UserSignInParam, response: Response, db: AsyncSession = Depends(get_db)
):
    await AuthService().sign_in(user=user, response=response, db=db)
    return {"message": "Sign In Succeed!"}


@router.delete(LOG_OUT)
async def logout(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    return await AuthService().logout(request=request, response=response, db=db)


# ********** REFRESH **********
@router.get(
    REFRESH,
    description="This endpoint is used to refresh token.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {
            "description": "Token has been refreshed successfully!",
        },
    },
)
async def refresh(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    await AuthService().refresh(request=request, response=response, db=db)
    return {"message": "Refresh Succeed!"}


# ********** GET ME **********
@router.get(
    GET_ME,
    dependencies=[Depends(dependencies.verify_access_token)],
    description="This endpoint is used to get user's information.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Get Me Succeed!", "model": ResGetMe},
    },
)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    return await AuthService().get_me(request=request, db=db)


@router.post(FORGOT)
async def forgot(email: str, db: AsyncSession = Depends(get_db)):
    return await AuthService().forgot_password(email=email, db=db)


@router.post(RESET)
async def reset(
    email: str, verify_code: str, new_password: str, db: AsyncSession = Depends(get_db)
):
    return await AuthService().reset_password(
        email=email, verify_code=verify_code, new_password=new_password, db=db
    )
