from fastapi import APIRouter, Depends, status
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .services import UserService
from app.schemas.user import CreateDemoUserParam

router = APIRouter(prefix="/users", tags=["User"])


# ********** Get List Users **********
@router.get(
    "/",
    description="This endpoint is used to get list user's information.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Get List Users Succeed!",
        },
    },
)
async def get_list_users(db: AsyncSession = Depends(get_db)):
    return await UserService().get_list_users(db=db)


# ********** Create Demo User **********
@router.post(
    "/",
    description="This endpoint is used to create a demo user account.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Create User Succeed!",
        },
    },
)
async def create_user(user: CreateDemoUserParam, db: AsyncSession = Depends(get_db)):
    return await UserService().create_user(user=user, db=db)
