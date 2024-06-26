from datetime import datetime, timedelta, timezone
import uuid
from app.configs.Clounfront import get_image_from_url
import bcrypt
import re
from dotenv import dotenv_values
from fastapi import HTTPException, status
import resend
import jwt

from app.schemas.auth import TokenPayload

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
    def verify_password(password: str, hash_password: str) -> bool:
        """
        Verify password using bcrypt
        """
        password_byte: bytes = password.encode("utf-8")
        hash_password_byte: bytes = hash_password.encode("utf-8")
        return bcrypt.checkpw(password_byte, hash_password_byte)

    @staticmethod
    def verify_email(*, send_from: str, send_to: str, token: str):
        """
        Send email to verify user email
        """
        resend.api_key = config["RESEND_KEY"]
        path = config["VERIFY_PATH"]
        url = f"{path}?token={token}"
        params = {
            "from": send_from,
            "to": send_to,
            "subject": "Verify your account",
            "html": f'<a href="{url}">Click here to verify your account</a>',
        }
        try:
            email = resend.Emails.send(params=params)
            return email
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    @staticmethod
    def forgot_email(send_from: str, send_to: str, code: str):
        """
        Send email to forgot password
        """
        resend.api_key = config["RESEND_KEY"]
        params = {
            "from": send_from,
            "to": send_to,
            "subject": "Reset your password",
            "html": f"Your verification code is  {code}",
        }
        resend.Emails.send(params=params)

    @staticmethod
    def create_verify_token(user_id: str):
        """
        Create token to verify user email
        """
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
            decode = jwt.decode(token, key, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid Token")
        user_id: str = decode.get("user_id")
        return user_id

    def create_access_token(self, user: TokenPayload):
        key = config["ACCESS_TOKEN_SECRET"] or "secret"
        seconds = config["ACCESS_TOKEN_EXPIRE"] or 600
        seconds = int(seconds)
        expire = self.__expire_time(seconds=seconds)
        user_id = str(user.id)
        role_id = str(user.role_id)
        payload = {"id": user_id, "role_id": role_id, "exp": expire}
        token = jwt.encode(
            payload=payload,
            key=key,
            algorithm=algorithm,
        )
        return token

    def create_refresh_token(self, user: TokenPayload):
        key = config["REFRESH_TOKEN_SECRET"] or "secret"
        seconds = config["REFRESH_TOKEN_EXPIRE"] or 604800
        seconds = int(seconds)
        expire = self.__expire_time(seconds)
        user_id = str(user.id)
        role_id = str(user.role_id)
        payload = {"id": user_id, "role_id": role_id, "exp": expire}
        token = jwt.encode(payload, key, algorithm)
        return token

    @staticmethod
    def verify_access_token(token: str):
        secret = config["ACCESS_TOKEN_SECRET"] or "secret"
        try:
            decode = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid access token. Please Re-login"
            )
        return decode

    @staticmethod
    def verify_refresh_token(token: str):
        secret = config["REFRESH_TOKEN_SECRET"] or "secret"
        try:
            decode = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Invalid refresh token. Please Re-login"
            )
        return decode

    @staticmethod
    def convert_str_to_UUID(id: str):
        return uuid.UUID(id)

    @staticmethod
    def __expire_time(seconds: int):
        return datetime.now(timezone.utc) + timedelta(seconds=seconds)

    @staticmethod
    def correct_fullname(first_name: str, last_name: str):
        """
        Check and correct user fullname:
            + remove redundant spaces
            + capitalize the first letter
        """
        fullname = first_name.lower().strip() + " " + last_name.lower().strip()
        while fullname.find("  ") != -1:
            fullname = fullname.replace("  ", " ")
        fullname = fullname.title()
        return fullname

    @staticmethod
    def slugify(title: str):
        """
        Convert title to slug
        """
        slug = title.lower().strip()

        slug = re.sub(r"á|à|ả|ạ|ã|ă|ắ|ằ|ẳ|ẵ|ặ|â|ấ|ầ|ẩ|ẫ|ậ", "a", slug)
        slug = re.sub(r"é|è|ẻ|ẽ|ẹ|ê|ế|ề|ể|ễ|ệ", "e", slug)
        slug = re.sub(r"i|í|ì|ỉ|ĩ|ị/gi", "i", slug)
        slug = re.sub(r"ó|ò|ỏ|õ|ọ|ô|ố|ồ|ổ|ỗ|ộ|ơ|ớ|ờ|ở|ỡ|ợ", "o", slug)
        slug = re.sub(r"ú|ù|ủ|ũ|ụ|ư|ứ|ừ|ử|ữ|ự", "u", slug)
        slug = re.sub(r"ý|ỳ|ỷ|ỹ|ỵ", "y", slug)
        slug = re.sub(r"đ", "d", slug)
        slug = re.sub(
            r"/\`|\~|\!|\@|\#|\||\$|\%|\^|\&|\*|\(|\)|\+|\=|\,|\.|\/|\?|\>|\<|\'|\"|\:|\;|_/gi",
            "",
            slug,
        )
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = re.sub(r"^-+|-+$", "", slug)
        return slug

    @staticmethod
    def convert_image_to_url(thumbnail: str) -> str:
        DOMAIN_IMAGE = get_image_from_url(thumbnail)
        if DOMAIN_IMAGE:
            return DOMAIN_IMAGE
        return thumbnail


helper: Helper = Helper()
