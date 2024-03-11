from enum import Enum
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# class RoleName(str, Enum):
#     user = "User"
#     admin = "Admin"


class UserBase(BaseModel):
    email: str


class GetUserByEmailParam(UserBase):
    pass


class CreateUserParam(UserBase):
    password: str
    role_id: UUID


class UserResponse(UserBase):
    id: UUID
    role_id: str
    refresh_token: str | None = None
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

class CreateDemoUserParam(UserBase):
    password: str
    first_name: str
    last_name: str
    role_name: str
