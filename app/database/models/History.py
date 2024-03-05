from uuid import UUID
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

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    bill_id: Mapped[UUID] = mapped_column(
        "bill_id", Uuid, ForeignKey(Bill.id), nullable=False
    )

    user: Mapped[User] = relationship()
    bill: Mapped[Bill] = relationship()

    def __init__(self, id: UUID, user_id: UUID, bill_id: UUID):
        self.id = id
        self.user_id = user_id
        self.bill_id = bill_id

    def __repr__(self):
        return f"<History {self.id}>"
