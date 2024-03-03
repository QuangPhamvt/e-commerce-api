from datetime import datetime
from typing import List
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    Uuid,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


# PRODUCT TAG TABLE
product_tag = Table(
    "ProductTag",
    Base.metadata,
    Column("product_id", Uuid, ForeignKey("Product.id"), primary_key=True),
    Column("tag_id", Uuid, ForeignKey("Tag.id"), primary_key=True),
)


# PRODUCT TABLE
class Product(Base):
    """
    Product model
    """

    __tablename__ = "Product"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    original_price: Mapped[float] = mapped_column(Float)
    sell_price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    country: Mapped[str] = mapped_column(String(50))
    factory: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(12))
    category_id: Mapped[str] = mapped_column(Uuid, ForeignKey("Category.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    tags: Mapped[List["Tag"]] = relationship(
        secondary=product_tag, back_populates="products"
    )

    def __init__(self, id: str):
        print("Product model")
        self.id = id

    def __repr__(self):
        return f"<Product {self.name}>"


# CATEGORY TABLE
class Category(Base):
    """
    Category model
    """

    __tablename__ = "Category"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    parent_id: Mapped[str] = mapped_column(Uuid, nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    update_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="category"
    )

    def __init__(self, id: str):
        print("Category model")
        self.id = id

    def __repr__(self):
        return f"<Category {self.name}>"


# TAG TABLE
class Tag(Base):
    """
    Tag model
    """

    __tablename__ = "Tag"

    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    products: Mapped[List["Product"]] = relationship(
        secondary=product_tag, back_populates="tags"
    )

    def __init__(self, id: str):
        print("Tag model")
        self.id = id

    def __repr__(self):
        return f"<Tag {self.name}>"


# DEPOSIT_TYPE TABLE
class DepositType(Base):
    """
    DepositType model
    """

    __tablename__ = "DepositType"

    id: Mapped[str] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)
    value: Mapped[float] = mapped_column("value", Float)
    fee: Mapped[float] = mapped_column("fee", Float)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.today()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    def __init__(self, id: str):
        print("DepositType model")
        self.id = id

    def __repr__(self):
        return f"<DepositType {self.name}>"
