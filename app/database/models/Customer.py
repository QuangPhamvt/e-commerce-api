from uuid import UUID
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from .User import User


# BIO TABLE
class Bio(Base):
    """
    Bio model
    """

    __tablename__ = "Bio"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    username: Mapped[str] = mapped_column("username", String(50))
    fullname: Mapped[str] = mapped_column("fullname", String(50))
    phone_number: Mapped[str] = mapped_column("phone_number", String(15))
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    def __init__(
        self, id: UUID, user_id: UUID, username: str, fullname: str, phone_number: str
    ):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.fullname = fullname
        self.phone_number = phone_number
        self.created_at = datetime.now()

    def __repr__(self):
        return f"<Bio {self.id}>"
