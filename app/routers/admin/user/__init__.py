from fastapi import APIRouter, Depends
from uuid import UUID
from app.configs.constants import USER, USER_PATH, USER_PREFIX
from app.dependencies.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import CreateUserParam
from app.services.user import UserService

CREATE_USER = USER_PATH["CREATE_USER"]
GET_USER = USER_PATH["GET_USER"]
UPDATE_USER = USER_PATH["UPDATE_USER"]
DELETE_USER = USER_PATH["DELETE_USER"]


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
async def get_user( db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_all()

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
async def create_user(body: CreateUserParam, db: AsyncSession = Depends(get_db)):
    return await UserService(db).create(body)


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
async def update_user(id: str, new_password: str, db: AsyncSession = Depends(get_db)):
    return await UserService(db).update_user(id,new_password)

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
                        "detail": "Delete User Succeed!"
                    }
                }
            },
        }
    },
)
async def delete_user(id: UUID, db: AsyncSession = Depends(get_db)):
    return await UserService(db).delete_user(id)







