from datetime import datetime
from typing import List
from uuid import UUID
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.database.models.Product import DepositType, Product
from .User import User


# BILL TABLE
class Bill(Base):
    """
    Bill model
    """

    __tablename__ = "Bill"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        "user_id", Uuid, ForeignKey(User.id), nullable=False
    )
    payos_id: Mapped[int] = mapped_column("payos_id", Integer, unique=True)
    customer_province: Mapped[str] = mapped_column(
        "customer_province", String(50), nullable=False
    )
    customer_district: Mapped[str] = mapped_column(
        "customer_district", String(50), nullable=False
    )
    customer_ward: Mapped[str] = mapped_column(
        "customer_ward", String(50), nullable=False
    )
    customer_address: Mapped[str] = mapped_column(
        "customer_address", String(255), nullable=False
    )
    customer_fullname: Mapped[str] = mapped_column(
        "customer_name", String(50), nullable=False
    )
    customer_phone_number: Mapped[str] = mapped_column(
        "customer_phone", String(15), nullable=False
    )
    product_price: Mapped[float] = mapped_column("product_price", Float, nullable=False)
    additional_fees: Mapped[List["AdditionalFee"]] = relationship(back_populates="bill")
    deposit_type_id: Mapped[UUID] = mapped_column(
        ForeignKey(DepositType.id), nullable=True
    )
    deposit_type: Mapped[DepositType] = relationship(back_populates="bills")
    status: Mapped[str] = mapped_column("status", String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, default=datetime.now(), nullable=False
    )

    user: Mapped[User] = relationship()
    bill_details: Mapped[List["BillDetail"]] = relationship(
        "BillDetail", back_populates="bill"
    )

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        customer_province: str,
        customer_district: str,
        customer_ward: str,
        customer_address: str,
        customer_fullname: str,
        customer_phone_number: str,
        product_price: float,
        status: str,
        payos_id: int,
        deposit_type_id: UUID | None = None,
    ):
        self.id = id
        self.user_id = user_id
        self.customer_province = customer_province
        self.customer_district = customer_district
        self.customer_ward = customer_ward
        self.customer_address = customer_address
        self.customer_fullname = customer_fullname
        self.customer_phone_number = customer_phone_number
        self.product_price = product_price
        self.status = status
        self.payos_id = payos_id
        if deposit_type_id:
            self.deposit_type_id = deposit_type_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __repr__(self):
        return f"<Bill {self.id}>"


# BILLDETAIL TABLE
class BillDetail(Base):
    """
    BillDetail model
    """

    __tablename__ = "BillDetail"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    bill_id: Mapped[UUID] = mapped_column(
        "bill_id", Uuid, ForeignKey(Bill.id), nullable=False
    )
    product_id: Mapped[UUID] = mapped_column(
        "product_id", Uuid, ForeignKey(Product.id), nullable=False
    )
    quantity: Mapped[int] = mapped_column("quantity", Integer, nullable=False)
    price: Mapped[float] = mapped_column("price", Float, nullable=False)

    bill: Mapped[Bill] = relationship("Bill", back_populates="bill_details")
    product: Mapped[Product] = relationship()

    def __init__(
        self, id: UUID, bill_id: UUID, product_id: UUID, quantity: int, price: float
    ):
        self.id = id
        self.bill_id = bill_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"<BillDetail {self.id}>"


# Additional Table


class AdditionalFee(Base):
    """
    Additional Fee model
    """

    __tablename__ = "AdditionalFee"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    description: Mapped[str] = mapped_column("description", String(255), nullable=False)
    value: Mapped[float] = mapped_column("value", Float, nullable=False)
    bill_id: Mapped[UUID] = mapped_column(ForeignKey(Bill.id), nullable=False)
    bill: Mapped["Bill"] = relationship(back_populates="additional_fees")
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, default=datetime.now(), nullable=False
    )
