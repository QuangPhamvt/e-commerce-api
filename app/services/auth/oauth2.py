from fastapi import Depends, HTTPException
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO
from starlette.requests import Request
from app.configs.constants import FACEBOOK_ID, FACEBOOK_SECRET
from app.configs.constants import GOOGLE_ID, GOOGLE_SECRET
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User

class GoogleAuth:
    def __init__(self):
        self.google_sso = GoogleSSO(GOOGLE_ID, GOOGLE_SECRET, "http://localhost:8000/api/v1/auth/google/callback", allow_insecure_http=True, use_state=True)
        self.data = None

    async def google_login(self, request: Request):
        return await self.google_sso.get_login_redirect(
            redirect_uri=request.url_for("google_callback"),
            params={"prompt": "consent", "access_type": "offline"}
        )
    async def google_callback(self,request: Request):
        return await self.google_sso.verify_and_process(request)     

class FacebookAuth:
    def __init__(self):
        self.facebook_sso = FacebookSSO(FACEBOOK_ID, FACEBOOK_SECRET, "http://localhost:8000/api/v1/auth/facebook/callback/", allow_insecure_http=True, scope="email,public_profile")
        self.user = None

    async def facebook_login(self):
        with self.facebook_sso:
            return await self.facebook_sso.get_login_redirect()

    async def facebook_callback(self,request: Request):
        with self.facebook_sso:
            user = await self.facebook_sso.verify_and_process(request)
            return user
