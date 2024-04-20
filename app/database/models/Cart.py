from uuid import UUID
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from .User import User
from .Product import Product


# CART TABLE
class Cart(Base):
    """
    Cart model
    """

    __tablename__ = "Cart"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    product_id: Mapped[UUID] = mapped_column(
        "product_id", Uuid, ForeignKey(Product.id), nullable=False
    )
    quantity: Mapped[int] = mapped_column("quantity", Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    def __init__(self, id: UUID, user_id: UUID, product_id: UUID, quantity: int):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.created_at = datetime.now()

    def __repr__(self):
        return f"<Cart {self.id}>"

    def asdict(self):
        return {
            "id": self.id,
            "quantity": self.quantity,
            "user_id": self.user_id,
        }
