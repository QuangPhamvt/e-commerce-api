from uuid import UUID
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .User import User


# CUSTOMER ADDRESS TABLE
class CustomerAddress(Base):
    """
    Customer Address Model
    """

    __tablename__ = "CustomerAddresses"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    fullname: Mapped[str] = mapped_column("fullname", String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(
        "phone_number", String(15), nullable=False
    )
    province: Mapped[str] = mapped_column("province", String(50), nullable=False)
    district: Mapped[str] = mapped_column("district", String(50), nullable=False)
    street: Mapped[str] = mapped_column("street", String(50), nullable=False)
    is_default: Mapped[bool] = mapped_column("is_default", Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    user: Mapped[User] = relationship()

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        fullname: str,
        phone_number: str,
        province: str,
        district: str,
        street: str,
        is_default: bool,
    ):
        self.id = id
        self.user_id = user_id
        self.fullname = fullname
        self.phone_number = phone_number
        self.province = province
        self.district = district
        self.street = street
        self.is_default = is_default
        self.created_at = datetime.now()

    def __repr__(self):
        return f"<CustomerAddress {self.id}>"
