from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class GetUserByEmailParam(UserBase):
    pass


class CreateUserParam(UserBase):
    password: str
    role_id: UUID


class UserResponse(UserBase):
    id: str
    role_id: str
    refresh_token: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
