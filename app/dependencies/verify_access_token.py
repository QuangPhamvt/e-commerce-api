from fastapi import Depends
from fastapi.security import APIKeyCookie

from app.utils.helper import Helper

access_token = APIKeyCookie(name="access_token", auto_error=False)


async def verify_access_token(access_token: str = Depends(access_token)):
    Helper.verify_access_token(token=access_token)
    return


async def get_me(access_token: str = Depends(access_token)):
    user = Helper.verify_access_token(token=access_token)
    user_id = Helper.convert_str_to_UUID(user.get("id"))
    return user_id
