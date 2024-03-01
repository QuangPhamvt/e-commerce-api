from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Uuid
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

    id: Mapped[str] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[str] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    product_id: Mapped[str] = mapped_column(
        "product_id", Uuid, ForeignKey(Product.id), nullable=False
    )
    quantity: Mapped[int] = mapped_column("quantity", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    def __init__(self, user_id: str):
        self.user_id = user_id

    def __repr__(self):
        return f"<Cart {self.id}>"
