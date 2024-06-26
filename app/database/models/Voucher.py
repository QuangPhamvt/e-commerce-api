from datetime import datetime
from uuid import UUID
from sqlalchemy import String, Float, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


# VOUCHER TABLE
class Voucher(Base):
    """
    Voucher model
    """

    __tablename__ = "Voucher"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    discount: Mapped[float] = mapped_column(Float)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(12))
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    upate_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __init__(
        self,
        id: UUID,
        code: str,
        discount: float,
        start_date: datetime,
        end_date: datetime,
        status: str,
    ):
        print("Voucher model")
        self.id = id
        self.code = code
        self.discount = discount
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.create_at = datetime.today()

    def __repr__(self):
        return f"<Voucher {self.code}>"
