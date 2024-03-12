from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BioBase(BaseModel):
    user_id: UUID
    username: str
    fullname: str
    phone_number: str

class CreateBioParam(BioBase):
    pass

class Bio(BioBase):
    id: UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None
