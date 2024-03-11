from fastapi import APIRouter, Depends, status
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.responses import ResBadRequest
from .services import UserService
from app.schemas.user import CreateDemoUserParam
from app.configs.constants import USER, USER_PREFIX, USER_PATH

GET_LIST_USERS = USER_PATH["GET_LIST_USERS"]
CREATE_DEMO_USER = USER_PATH["CREATE_DEMO_USER"]

router = APIRouter(
    prefix=USER_PREFIX, 
    tags=[USER],
    responses={
        400: {
            "model": ResBadRequest,
            "description": "Description when error occurs",
        },
    },    
)

# ********** Get List Users **********
@router.get(
    GET_LIST_USERS,
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
    CREATE_DEMO_USER,
    description="This endpoint is used to create a demo user account.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Create User Succeed!",
        },
    },
)
async def create_demo_user(user: CreateDemoUserParam, db: AsyncSession = Depends(get_db)):
    return await UserService().create_demo_user(user=user, db=db)
