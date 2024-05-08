from fastapi import Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from app.configs.constants import FACEBOOK_ID, FACEBOOK_SECRET
from app.configs.constants import GOOGLE_ID, GOOGLE_SECRET
from app.database.crud.user_crud import UserCRUD
from app.dependencies import get_db
from app.schemas.auth import UserSignUpParam

from app.services.auth import AuthService
from app.services.oauth.facebook_sso import FacebookSSO
from app.services.oauth.google_sso import GoogleSSO
from sqlalchemy.ext.asyncio import AsyncSession

class GoogleAuth:
    def __init__(self):
        self.google_sso = GoogleSSO(GOOGLE_ID, GOOGLE_SECRET, "http://localhost:8000/api/v1/auth/google/callback", allow_insecure_http=True, use_state=True)
        self.data = None

    async def google_login(self, request: Request):
        return await self.google_sso.get_login_redirect(
            redirect_uri=request.url_for("google_callback"),
            params={"prompt": "consent", "access_type": "offline"}
        )
    async def google_callback(self, request: Request, response: Response, db: AsyncSession = Depends(get_db)):
        """Get google data"""
        with self.google_sso:
            openid = await self.google_sso.verify_and_process(request)
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
    

class FacebookAuth:
    def __init__(self):
        self.facebook_sso = FacebookSSO(FACEBOOK_ID, FACEBOOK_SECRET, "http://localhost:8000/api/v1/auth/facebook/callback/", allow_insecure_http=True, scope="email,public_profile")
        self.user = None

    async def facebook_login(self):
        with self.facebook_sso:
            return await self.facebook_sso.get_login_redirect()

    async def facebook_callback(self, request: Request, response: Response, db: AsyncSession = Depends(get_db)):
        """Get facebook data"""
        with self.facebook_sso:
            openid = await self.facebook_sso.verify_and_process(request)
            if not openid:
                raise HTTPException(status_code=401, detail="Authentication failed")
        user = await UserCRUD(db).read_user_by_email(openid.email)
        if not user:
            """User not exists, sign up for them, after that get user info to login them in"""
            user_signup = UserSignUpParam(
                email=openid.email,
                password=openid.id, # Use the id get from facebook as default password
                fullname=openid.display_name
            )
            await AuthService().sign_up_instant_active(user_signup, db)
        
        """Now user exist, log them in"""
        response = RedirectResponse(url="/api/v1/auth/docs")
        await AuthService().sign_in_without_password(openid.email, response, db)
        return response


