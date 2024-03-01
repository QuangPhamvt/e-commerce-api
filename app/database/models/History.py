from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from .Bill import Bill
from .User import User


# HISTORY TABLE
class History(Base):
    """
    History model
    """

    __tablename__ = "History"

    id: Mapped[str] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    bill_id: Mapped[str] = mapped_column(
        "bill_id", Uuid, ForeignKey(Bill.id), nullable=False
    )

    user: Mapped[User] = relationship()
    bill: Mapped[Bill] = relationship()
