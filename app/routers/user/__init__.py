from fastapi import APIRouter, Depends, Request, Response, status
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .services import UserService

router = APIRouter(prefix="/users", tags=["User"])

# ********** Get List Users **********
@router.get("/",
    description="This endpoint is used to get list user's information.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Get List Users Succeed!",
        },
    },
)
async def get_list_users(request: Request, db: AsyncSession = Depends(get_db)):
    return await UserService.get_list_users(db)