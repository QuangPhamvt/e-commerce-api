from fastapi import APIRouter, Depends
from app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.role import CreateRoleParam
from ..services.role_service import role_service

router = APIRouter(prefix="/roles", tags=["Role"])


@router.post("")
async def create_role(role: CreateRoleParam, db: AsyncSession = Depends(get_db)):
    return await role_service.create(role=role, db=db)
