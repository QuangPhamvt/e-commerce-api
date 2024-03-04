from uuid import UUID
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.database.models import User


user_global_notification = Table(
    "UserGlobalNotification",
    Base.metadata,
    Column("user_id", ForeignKey("User.id"), primary_key=True),
    Column("notification_id", ForeignKey("Notification.id"), primary_key=True),
    Column("is_read", Boolean, default=False),
)


# NOTIFICATION TABLE
class Notification(Base):
    """
    Notification model
    """

    __tablename__ = "Notification"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    title: Mapped[str] = mapped_column("title", String(255))
    content: Mapped[str] = mapped_column("content", String(255))
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )

    def __init__(self, id: UUID, title: str, content: str):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = datetime.now()

    def __repr__(self):
        return "<Notification %r>" % (self.id)


class UserNotification(Base):
    """
    UserNotification model
    """

    __tablename__ = "UserNotification"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("User.id"))
    content: Mapped[str] = mapped_column(Text(255))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship("User", back_populates="user_notifications")

    def __init__(
        self, id: UUID, title: str, user_id: UUID, content: str, is_read: bool
    ):
        self.id = id
        self.title = title
        self.user_id = user_id
        self.content = content
        self.is_read = is_read

    def __repr__(self):
        return "<UserNotification %r>" % (self.user_id)
