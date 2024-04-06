from fastapi import APIRouter, Depends
from app.configs.constants import USER, USER_PATH, USER_PREFIX
from app.dependencies.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import CreateDemoUserParam
from app.services.user import UserService

CREATE_USER = USER_PATH["CREATE_USER"]
GET_USER = USER_PATH["GET_USER"]
UPDATE_USER = USER_PATH["UPDATE_USER"]
DELETE_USER = USER_PATH["DELETE_USER"]

GET_LIST_USERS = USER_PATH["GET_LIST_USERS"]
CREATE_DEMO_USER = USER_PATH["CREATE_DEMO_USER"]

router = APIRouter(prefix=USER_PREFIX, tags=[USER])

@router.get(
    GET_USER,
    description="This endpoint is used to get user by id.",
    status_code=200,
    responses={
        200: {
            "description": "Get User Succeed!",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Get User Succeed"
                    }
                }
            }    
        }
    }
)
async def get_user(id: str, db: AsyncSession = Depends(get_db)):
    return await UserService().get_by_id(id, db)

@router.post(
    CREATE_USER,
    description="This endpoint is used to create a new user.",
    status_code=201,
    responses={
        201: {
            "description": "Create User Succeed!",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Create User Succeed!",
                    }
                }
            },
        }
    },
)
async def create_user(body: CreateDemoUserParam, db: AsyncSession = Depends(get_db)):
    return await UserService().create_user(body, db)


@router.put(
    UPDATE_USER,
    description="This endpoint is used to update user by id.",
    status_code=200,
    responses={
        200: {
            "description": "Update User Succeed!",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Update User Succeed!",
                    }
                }
            },
        }
    },
)
async def update_user(id: str, body: CreateDemoUserParam, db: AsyncSession = Depends(get_db)):
    return await UserService().update_user(id, body, db)

@router.delete(
    DELETE_USER,
    description="This endpoint is used to delete user by id.",
    status_code=200,
    responses={
        200: {
            "description": "Delete User Succeed!",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Delete User Succeed!",
                    }
                }
            },
        }
    },
)
async def delete_user(id: str, db: AsyncSession = Depends(get_db)):
    return await UserService().delete_user(id, db)




@router.get(
    GET_LIST_USERS,
    description="This endpoint is used to get list of users.",
    status_code=200,
    responses={
        200: {
            "detail": "Get List User Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "email": "user@example.com",
                            "id": "67b5ab15-ee53-446e-8fe5-7ab13bac7ff7",
                            "role_id": "83j3cm89-ee53-446e-8fe5-7ab13bac7ff7",
                            "is_active": True,
                        }
                    ]
                }
            },
        }
    },
)
async def get_list_user(db: AsyncSession = Depends(get_db)):
    return await UserService().get_list_users(db)


@router.post(
    CREATE_DEMO_USER,
    description="This endpoint is used to create a demo user.",
    status_code=201,
    responses={
        201: {
            "detail": "Get List User Succeed!",
            "content": {
                "description": "Create User Succeed!",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Create User Succeed!",
                        }
                    }
                },
            },
        }
    },
)
async def create_demo_user(
    body: CreateDemoUserParam, db: AsyncSession = Depends(get_db)
):
    return await UserService().create_demo_user(body, db)
