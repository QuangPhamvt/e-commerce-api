from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


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
