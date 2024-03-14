from pydantic import BaseModel


class ResBadRequest(BaseModel):
    message: str


class Res201Resquest(BaseModel):
    detail: str
