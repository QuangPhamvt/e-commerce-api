from pydantic import BaseModel


class ResBadRequest(BaseModel):
    message: str
