from uuid import UUID
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .Bill import Bill


# DeliveryDetail TABLE
class DeliveryDetail(Base):
    """
    DeliveryAddress model
    """

    __tablename__ = "DeliveryDetail"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    bill_id: Mapped[UUID] = mapped_column(
        "bill_id", Uuid, ForeignKey(Bill.id), nullable=False
    )
    description: Mapped[str] = mapped_column("description", Text, nullable=False)
    status: Mapped[str] = mapped_column("status", String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, default=datetime.now(), nullable=False
    )

    bill: Mapped[Bill] = relationship()

    def __init__(self, id: UUID, bill_id: UUID, description: str, status: str):
        self.id = id
        self.bill_id = bill_id
        self.description = description
        self.status = status
        self.created_at = datetime.now()

    def __repr__(self):
        return f"<DeliveryAddress {self.id}>"
