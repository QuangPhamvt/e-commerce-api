from datetime import datetime, timedelta, timezone
import bcrypt
from dotenv import dotenv_values
from fastapi import HTTPException, status
import resend
import jwt
from app.configs.constants import (
    ACCESS_TOKEN_EXPIRE,
    ACCESS_TOKEN_SECRET,
    REFRESH_TOKEN_EXPIRE,
    REFRESH_TOKEN_SECRET,
)

from app.schemas.auth import AccessTokenPayload, RefreshTokenPayload

config = dotenv_values(".env")
salt = bcrypt.gensalt()
algorithm = "HS256"


class Helper:
    @staticmethod
    def hash_password(*, password: str) -> bytes:
        """
        Hash password using bcrypt
        """
        _byte: bytes = password.encode("utf-8")
        hash = bcrypt.hashpw(_byte, salt=salt)
        return hash

    @staticmethod
    def verify_password(*, password: str, hash_password: str) -> bool:
        _byte: bytes = password.encode("utf-8")
        hash_password_byte: bytes = hash_password.encode("utf-8")
        return bcrypt.checkpw(password=_byte, hashed_password=hash_password_byte)

    @staticmethod
    def verify_email(*, send_from: str, send_to: str, token: str):
        resend.api_key = config["RESEND_KEY"]
        path = config["VERIFY_PATH"]
        url = f"{path}?token={token}"
        params = {
            "from": send_from,
            "to": send_to,
            "subject": "Verify your account",
            "html": f'<a href="{url}">Click here to verify your account</a>',
        }
        email = resend.Emails.send(params=params)
        return email

    @staticmethod
    def create_verify_token(user_id: str):
        key: str = config["VERIFY_EMAIL_SECRET"] or "secret"
        token = jwt.encode(
            {"user_id": user_id},
            key,
            algorithm=algorithm,
        )
        return token

    @staticmethod
    def verify_token(token: str):
        key = config["VERIFY_EMAIL_SECRET"] or "key"
        try:
            decode = jwt.decode(jwt=token, key=key, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
            )
        return decode

    @staticmethod
    def __expire_time(seconds: int):
        return datetime.now(timezone.utc) + timedelta(seconds=seconds)

    def create_access_token(self, user_data: AccessTokenPayload):
        seconds = int(ACCESS_TOKEN_EXPIRE)
        expire = self.__expire_time(seconds=seconds)
        key = ACCESS_TOKEN_SECRET
        id = str(user_data.id)
        role_id = str(user_data.role_id)
        payload = {"id": id, "role_id": role_id, "exp": expire}
        token = jwt.encode(
            payload=payload,
            key=key,
            algorithm=algorithm,
        )
        return token

    def create_refresh_token(self, user_data: RefreshTokenPayload):
        seconds = int(REFRESH_TOKEN_EXPIRE)
        expire = self.__expire_time(seconds)
        key = REFRESH_TOKEN_SECRET
        id = str(user_data.id)
        role_id = str(user_data.role_id)
        payload = {"id": id, "role_id": role_id, "exp": expire}
        token = jwt.encode(
            payload=payload,
            key=key,
            algorithm=algorithm,
        )
        return token

    @staticmethod
    def verify_refresh_token(token: str):
        secret = REFRESH_TOKEN_SECRET
        try:
            decode = jwt.decode(jwt=token, key=secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token. Please Re-login",
            )
        return decode


helper: Helper = Helper()
