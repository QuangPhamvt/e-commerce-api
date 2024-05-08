from datetime import datetime
import uuid

from fastapi import HTTPException, status


def generate_uuid():
    return uuid.uuid4()


def generate_current_timestamp():
    return int(datetime.now().timestamp())


def convert_str_to_uuid(raw_id: str):
    try:
        new_uuid = uuid.UUID(raw_id)
        return new_uuid
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Id is not UUID type!")
