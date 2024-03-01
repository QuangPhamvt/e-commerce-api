from sqlalchemy import Column, Integer, String, Float
from app.database import Base


# ExchangeRate
class ExchangeRate(Base):
    """
    ExchangeRate model
    """

    __tablename__ = "ExchangeRate"

    id = Column(Integer, primary_key=True)
    currency = Column(String(20))
    rate = Column(Float)

    def __init__(self, currency=None, rate=None):
        self.currency = currency
        self.rate = rate

    def __repr__(self):
        return "<ExchangeRate %r>" % (self.currency)
