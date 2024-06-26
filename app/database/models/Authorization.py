from uuid import UUID
from app.database import Base
from typing import List
from sqlalchemy import String, Uuid, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import User


# AUTHORIZATION

role_permission = Table(
    "RolePermission",
    Base.metadata,
    Column("role_id", Uuid, ForeignKey("Role.id"), primary_key=True),
    Column("permission_id", Uuid, ForeignKey("Permission.id"), primary_key=True),
)


# ROLE TABLE
class Role(Base):
    """
    Role model
    """

    __tablename__ = "Role"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)

    permission: Mapped[List["Permission"]] = relationship(
        secondary=role_permission, back_populates="role"
    )

    users: Mapped[User] = relationship("User", back_populates="role")

    def __init__(self, id: UUID, name: str):
        print("Role model")
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Role {self.name}>"


# PERMISSION TABLE
class Permission(Base):
    """



    Permission model
    """

    __tablename__ = "Permission"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    path: Mapped[str] = mapped_column("path", String(50))
    method: Mapped[str] = mapped_column("method", String(50))

    role: Mapped[List["Role"]] = relationship(
        secondary=role_permission, back_populates="permission"
    )

    def __init__(self, id: UUID, path: str, method: str):
        print("Permission model")
        self.id = id
        self.path = path
        self.method = method

    def __repr__(self):
        return f"<Permission {self.path}>"
