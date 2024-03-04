import bcrypt
from dotenv import dotenv_values
from fastapi import HTTPException, status
import resend
import jwt

config = dotenv_values(".env")


class Helper:
    @staticmethod
    def hash_password(*, password: str) -> bytes:
        """
        Hash password using bcrypt
        """
        _byte: bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(_byte, salt=salt)
        return hash

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
            algorithm="HS256",
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


helper: Helper = Helper()
