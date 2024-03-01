from datetime import datetime
from sqlalchemy import DateTime, String, Uuid, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from ..database import Base
from .Authorization import Role


# USER TABLE
class User(Base):
    """
    User model
    """

    __tablename__ = "User"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hash_password: Mapped[str] = mapped_column(String(255))
    refresh_token: Mapped[str] = mapped_column(Text(), nullable=True)
    role_id: Mapped[int] = mapped_column(Uuid, ForeignKey("Role.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    role: Mapped[Role] = relationship("Role", back_populates="user")

    def __init__(self, id: str):
        print("User model")
        self.id = id

    def __repr__(self):
        return f"<User {self.email}>"


# RESET PASSWORD TABLE
class ResetPassword(Base):
    """
    ResetPassword model
    """

    __tablename__ = "ResetPassword"

    user_id: Mapped[int] = mapped_column(Uuid, ForeignKey("User.id"), primary_key=True)
    code: Mapped[str] = mapped_column(String(8))
    expire_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(self, id: int):
        print("ResetPassword model")
        self.id = id

    def __repr__(self):
        return f"<ResetPassword {self.code} {self.expire_at}>"
