from datetime import datetime
from pydantic import UUID4, BaseModel


class UserBase(BaseModel):
    email: str


class GetUserByEmailParam(UserBase):
    pass


class CreateUserParam(UserBase):
    password: str
    role_id: UUID4


class UserResponse(UserBase):
    id: str
    role_id: str
    refresh_token: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None
