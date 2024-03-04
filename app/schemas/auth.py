from uuid import UUID
from pydantic import BaseModel, EmailStr


class AuthBase(BaseModel):
    email: EmailStr
    password: str


class UserSignUpParam(AuthBase):
    pass


class UserSignInParam(AuthBase):
    pass


class AccessTokenPayload(BaseModel):
    id: UUID
    role_id: UUID


class RefreshTokenPayload(BaseModel):
    id: UUID
    role_id: UUID


class VerifyPayload(BaseModel):
    user_id: UUID
