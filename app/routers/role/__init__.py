from fastapi import APIRouter, Depends, status
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.responses import ResBadRequest
from app.schemas.role import CreateRoleParam
from .services import RoleService
from app.configs.constants import ROLE, ROLE_PREFIX, ROLE_PATH

GET_LIST_ROLES = ROLE_PATH["GET_LIST_ROLES"]
CREATE_ROLE = ROLE_PATH["CREATE_ROLE"]
DELETE_ROLE = ROLE_PATH["DELETE_ROLE"]
UPDATE_ROLE = ROLE_PATH["UPDATE_ROLE"]

router = APIRouter(
    prefix=ROLE_PREFIX, 
    tags=[ROLE],
    responses={
        400: {
            "model": ResBadRequest,
            "description": "Description when error occurs",
        },
    },    
)


@router.post(
    CREATE_ROLE,
    description="This endpoint is used to create new role.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Create role succeed!",
        },
    },    
)
async def create_role(role: CreateRoleParam, db: AsyncSession = Depends(get_db)):
    return await RoleService().create(role=role, db=db)

@router.get(
    GET_LIST_ROLES,
    description="This endpoint is used to get list roles.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Get list roles succeed!",
        },
    },
)
async def get_list_roles(db: AsyncSession = Depends(get_db)):
    return await RoleService().get_all(db=db)

@router.delete(
    DELETE_ROLE,
    description="This endpoint is used to delete role using role_id.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Delete role succeed!",
        },
    },        
)
async def delete_role(id: str, db: AsyncSession = Depends(get_db)):
    return await RoleService().delete(id=id, db=db)

@router.put(
    DELETE_ROLE,
    description="This endpoint is used to update role name using role_id.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Update role succeed!",
        },
    },
)
async def update_role(
    id: str, 
    role: CreateRoleParam, 
    db: AsyncSession = Depends(get_db)
):
    return await RoleService().update(id=id, new_role_name=role.name, db=db)