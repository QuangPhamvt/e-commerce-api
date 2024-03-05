from fastapi import Depends
from fastapi.security import APIKeyCookie

from app.utils.helper import Helper

access_token = APIKeyCookie(name="access_token")


async def verify_access_token(access_token: str = Depends(access_token)):
    Helper.verify_access_token(token=access_token)
    return
