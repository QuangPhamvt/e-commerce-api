from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .User import User


# TICKET TABLE
class Ticket(Base):
    """
    Ticket model
    """

    __tablename__ = "Ticket"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    title: Mapped[str] = mapped_column("title", String(255), nullable=False)
    content: Mapped[str] = mapped_column("content", String(255), nullable=False)
    status: Mapped[str] = mapped_column("status", String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    user: Mapped[User] = relationship()

    def __init__(self, id: UUID, user_id: UUID, title: str, content: str, status: str):
        print("Ticket model")
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.status = status
        self.created_at = datetime.now()

    def __repr__(self):
        return f"<Ticket {self.id}>"
