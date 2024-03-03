from pydantic import BaseModel, EmailStr


class AuthBase(BaseModel):
    email: EmailStr
    password: str


class UserSignUpParam(AuthBase):
    pass


class VerifyPayload(BaseModel):
    user_id: str
