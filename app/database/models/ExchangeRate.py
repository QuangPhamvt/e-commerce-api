from uuid import UUID
from sqlalchemy import String, Float, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


# ExchangeRate
class ExchangeRate(Base):
    """
    ExchangeRate model
    """

    __tablename__ = "ExchangeRate"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    currency: Mapped[str] = mapped_column("currency", String(20))
    rate: Mapped[float] = mapped_column("rate", Float)

    def __init__(self, id: UUID, currency: str, rate: float):
        self.id = id
        self.currency = currency
        self.rate = rate

    def __repr__(self):
        return "<ExchangeRate %r>" % (self.currency)
