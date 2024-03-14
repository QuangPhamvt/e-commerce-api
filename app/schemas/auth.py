from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class AuthBase(BaseModel):
    email: EmailStr = Field(
        title="Email",
        description="Email of user",
        examples=["quangpm220503vt@gmail.com"],
    )
    password: str = Field(
        title="Password", description="Password of user", examples=["123456"]
    )


class UserSignUpParam(AuthBase):
    fullname: str = Field(
        title="Fullname",
        description="Fullname of user",
        examples=["Pham Minh Quang"],
    )
    pass


class UserSignInParam(AuthBase):
    pass


class VerifyParam(BaseModel):
    token: str = Field(
        title="Token",
        description="Token to verify user's email",
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImMwMzIwMzIwLWYwMzItNDMyMC1hMzMyLTQzMjAzMjAzMjAzMiIsInJvbGVfaWQiOiJjMDMyMDMyMC1mMDMyLTQzMjAtYTMzMi00MzIwMzIwMzIwMzIiLCJpYXQiOjE2MzIwMzIwMzJ9."
        ],
    )
    pass


class TokenPayload(BaseModel):
    id: UUID
    role_id: UUID


class VerifyPayload(BaseModel):
    user_id: UUID


class ResGetMe(BaseModel):
    id: UUID
    role_id: UUID
    email: EmailStr
    is_active: bool
    pass
