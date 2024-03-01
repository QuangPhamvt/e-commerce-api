from datetime import datetime
from sqlalchemy import DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


# PROMOTION TABLE
class Promotion(Base):
    """
    Promotion model
    """

    __tablename__ = "Promotion"

    id: Mapped[str] = mapped_column("id", Uuid, primary_key=True)
    deposit_type_id: Mapped[str] = mapped_column(
        "deposit_type_id", Uuid, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=False)
