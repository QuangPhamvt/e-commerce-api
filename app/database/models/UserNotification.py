from sqlalchemy import Boolean, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .User import User


# UserNotification TABLE
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

    user: Mapped[User] = relationship(back_populates="user_notifications")

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "<UserNotification %r>" % (self.user_id)
