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

    id: Mapped[str] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    username: Mapped[str] = mapped_column("username", String(50))
    fullname: Mapped[str] = mapped_column("fullname", String(50))
    phone_number: Mapped[str] = mapped_column("phone_number", String(15))
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    def __init__(self, user_id: str):
        self.user_id = user_id

    def __repr__(self):
        return f"<Bio {self.id}>"
