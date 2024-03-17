from uuid import UUID
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.utils.helper import helper


class Logout:
    @staticmethod
    async def logout(request: Request, response: Response, db: AsyncSession):
        refresh_token = request.cookies.get("refresh_token")
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        if refresh_token:
            payload = helper.verify_refresh_token(refresh_token)
            user_id = UUID(payload["id"])
            await user_crud.update_refresh_token(user_id, None, db)
        return {"detail": "Logout Succeed!"}
