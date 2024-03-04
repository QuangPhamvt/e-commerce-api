from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, String, Uuid, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.Notification import UserNotification


from ..database import Base
from .Authorization import Role


# USER TABLE
class User(Base):
    """
    User model
    """

    __tablename__ = "User"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[bytes] = mapped_column(String(255))
    refresh_token: Mapped[str] = mapped_column(Text(), nullable=True)
    role_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("Role.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    role: Mapped[Role] = relationship("Role", back_populates="users")

    user_notifications: Mapped[UserNotification] = relationship(
        "UserNotification", back_populates="user"
    )

    def __init__(
        self, id: UUID, email: str, hash_password: bytes, role_id: UUID, is_active: bool
    ):
        print("User model")
        self.id = id
        self.email = email
        self.hash_password = hash_password
        self.role_id = role_id
        self.is_active = is_active
        self.create_at = datetime.now()

    def __repr__(self):
        return f"<User {self.email}>"


# RESET PASSWORD TABLE
class ResetPassword(Base):
    """
    ResetPassword model
    """

    __tablename__ = "ResetPassword"

    user_id: Mapped[Uuid] = mapped_column(Uuid, ForeignKey("User.id"), primary_key=True)
    code: Mapped[str] = mapped_column(String(8))
    expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(self, id: Uuid, code: str, expire_at: datetime):
        print("ResetPassword model")
        self.id = id
        self.code = code
        self.expire_at = expire_at
        self.create_at = datetime.now()

    def __repr__(self):
        return f"<ResetPassword {self.code} {self.expire_at}>"
