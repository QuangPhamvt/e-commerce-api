from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


# PROMOTION TABLE
class Promotion(Base):
    """
    Promotion model
    """

    __tablename__ = "Promotion"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    deposit_type_id: Mapped[UUID] = mapped_column(
        "deposit_type_id", Uuid, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=False)

    def __init__(self, id: UUID, deposit_type_id: UUID):
        print("Promotion model")
        self.id = id
        self.deposit_type_id = deposit_type_id
        self.created_at = datetime.now()
