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

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def __init__(self, message=None, user_id=None):
        self.message = message
        self.user_id = user_id

    def __repr__(self):
        return "<Notification %r>" % (self.message)


class UserNotification(Base):
    """
    UserNotification model
    """

    __tablename__ = "UserNotification"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[User] = mapped_column(Uuid, ForeignKey("User.id"))
    content: Mapped[str] = mapped_column(Text(255))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[User] = relationship("User", back_populates="user_notifications")

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "<UserNotification %r>" % (self.user_id)
