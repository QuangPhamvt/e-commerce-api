from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response, Security, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from app.database.crud.user_crud import UserCRUD
from app.dependencies import get_db, get_current_username, verify_access_token
from app.schemas.auth import ResGetMe, UserSignInParam, UserSignUpParam, VerifyParam
from app.services.auth import AuthService
from app.utils.helper import helper
from app.configs.constants import AUTH, AUTH_PATH, GOOGLE_ID, GOOGLE_SECRET
from app.schemas.responses import ResBadRequest
from app.configs.documentations import AUTH_DOCUMENTATIONS
from fastapi_sso.sso.google import GoogleSSO

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
google_sso = GoogleSSO(GOOGLE_ID, GOOGLE_SECRET, "http://localhost:8000/api/v1/auth/google/callback", allow_insecure_http=True)

@router.get(GOOGLE_LOGIN)
async def google_login():
    return await google_sso.get_login_redirect()

@router.get(GOOGLE_CALLBACK)
async def google_callback(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    """Get google data"""
    with google_sso:
        openid = await google_sso.verify_and_process(request)
        if not openid:
            raise HTTPException(status_code=401, detail="Authentication failed")
    user = await UserCRUD(db).read_user_by_email(openid.email)

    if not user:
        """User not exists, sign up for them, after that get user info to login them in"""
        user_signup = UserSignUpParam(
            email=openid.email,
            password=openid.id, # Use the id get from google as default password
            fullname=openid.display_name
        )
        await AuthService().sign_up_instant_active(user_signup, db)
    
    """Now user exist, log them in"""
    response = RedirectResponse(url="/api/v1/auth/docs")
    await AuthService().sign_in_without_password(openid.email, response, db)
    return response


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
