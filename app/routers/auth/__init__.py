from fastapi import APIRouter, Depends, FastAPI, Request, Response, Security, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_username, verify_access_token
from app.schemas.auth import ResGetMe, UserSignInParam, UserSignUpParam, VerifyParam
from app.services.auth import AuthService

from app.services.oauth import OauthService
from app.utils.helper import helper
from app.configs.constants import AUTH, AUTH_PATH
from app.schemas.responses import ResBadRequest
from app.configs.documentations import AUTH_DOCUMENTATIONS

SIGN_UP = AUTH_PATH["SIGN_UP"]
VERIFY = AUTH_PATH["VERIFY"]
SIGN_IN = AUTH_PATH["SIGN_IN"]
LOG_OUT = AUTH_PATH["LOG_OUT"]
REFRESH = AUTH_PATH["REFRESH"]
GET_ME = AUTH_PATH["GET_ME"]
FORGOT = AUTH_PATH["FORGOT"]
RESET = AUTH_PATH["RESET"]
GOOGLE_LOGIN = AUTH_PATH["GOOGLE_LOGIN"]
GOOGLE_CALLBACK = AUTH_PATH["GOOGLE_CALLBACK"]
GOOGLE_LOGOUT = AUTH_PATH["GOOGLE_LOGOUT"]
FACEBOOK_LOGIN = AUTH_PATH["FACEBOOK_LOGIN"]
FACEBOOK_CALLBACK = AUTH_PATH["FACEBOOK_CALLBACK"]

router = APIRouter(
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
    res = await AuthService().sign_up(user, db)
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
    payload = helper.verify_token(token)
    await AuthService().verify(payload, db)
    return {"detail": "Verify Succeed!"}


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
    await AuthService().sign_in(user, response, db)
    return {"detail": "Sign In Succeed!"}


@router.delete(LOG_OUT)
async def logout(
    request: Request, response: Response, db: AsyncSession = Depends(get_db)
):
    return await AuthService().logout(request, response, db)


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
    await AuthService().refresh(request, response, db)
    return {"detail": "Refresh Succeed!"}


# ********** GET ME **********
@router.get(
    GET_ME,
    dependencies=[Depends(verify_access_token)],
    description="This endpoint is used to get user's information.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Get Me Succeed!", "model": ResGetMe},
    },
)
async def get_me(request: Request, db: AsyncSession = Depends(get_db)):
    return await AuthService().get_me(request, db)


# ********** FORGOT **********
@router.post(FORGOT)
async def forgot(email: str, db: AsyncSession = Depends(get_db)):
    return await AuthService().forgot_password(email, db)


# ********** RESET **********
@router.post(RESET)
async def reset(
    email: str, verify_code: str, new_password: str, db: AsyncSession = Depends(get_db)
):
    return await AuthService().reset_password(email, verify_code, new_password, db)


# ********** OAUTH **********

@router.get(GOOGLE_LOGIN)
async def google_login(request: Request):
    return await OauthService().google_login(request)

@router.get(GOOGLE_CALLBACK)
async def google_callback(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    return await OauthService().google_callback(request, response, db)

@router.get(FACEBOOK_LOGIN)
async def google_login():
    return await OauthService().facebook_login()

@router.get(FACEBOOK_CALLBACK)
async def google_callback(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    return await OauthService().facebook_callback(request, response, db)


# Auth Api
auth_api = FastAPI(docs_url=None, **AUTH_DOCUMENTATIONS)

auth_api.include_router(router)


@auth_api.get("")
def read_auth():
    return {
        "message": "Hello World from auth api",
    }


@auth_api.get("/docs", include_in_schema=False)
async def get_swagger_auth_documentation(
    __username__: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/auth/openapi.json",
        title="E-commerce API Documentation",
    )


@auth_api.get("/openapi.json", include_in_schema=False)
async def auth_openapi(__username__: str = Depends(get_current_username)):
    get_openapi(title=auth_api.title, version=auth_api.version, routes=auth_api.routes)
