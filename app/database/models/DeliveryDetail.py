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

    id: Mapped[str] = mapped_column("id", Uuid, primary_key=True)
    bill_id: Mapped[str] = mapped_column(
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

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<DeliveryAddress {self.id}>"
