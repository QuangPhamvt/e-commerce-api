from typing import Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# class RoleName(str, Enum):
#     user = "User"
#     admin = "Admin"


class UserBase(BaseModel):
    email: str = Field(
        title="Email", description="Email of user", examples=["21522517@gm.uit.edu.vn"]
    )


class GetUserByEmailParam(UserBase):
    pass


class CreateUserParam(UserBase):
    id: UUID
    email: str
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
    password: str = Field(
        title="Password",
        description="Password for new user",
        min_length=8,
        examples=["12345678"],
    )
    first_name: str = Field(
        title="First name",
        description="First name of new user",
        examples=["Pham"],
    )
    last_name: str = Field(
        title="Last name",
        description="Last name of new user",
        examples=["Minh Quang"],
    )
    role_name: str = Field(
        title="Role name",
        description="Role name of new user",
        examples=["User"],
    )


class ResGetListUsers(BaseModel):
    id: UUID
    email: str
    role_id: UUID
    is_active: bool
    created_at: datetime
    bio_id: UUID
    username: str
    full_name: str
    phone_number: str
    role: str
    address: list[Any]
