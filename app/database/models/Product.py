from datetime import datetime
from typing import List
from uuid import UUID
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
from app.database.models import Bill


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

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(255), unique=True)
    description: Mapped[str] = mapped_column("description", Text(), nullable=True)
    original_price: Mapped[float] = mapped_column(
        "original_price", Float, nullable=True
    )
    sell_price: Mapped[float] = mapped_column("sell_price", Float, nullable=True)
    quantity: Mapped[int] = mapped_column("quantity", Integer, nullable=True)
    slug: Mapped[str] = mapped_column("slug", String(255), unique=True)
    country: Mapped[str] = mapped_column("country", String(50), nullable=True)
    factory: Mapped[str] = mapped_column("factory", String(50), nullable=True)
    status: Mapped[str] = mapped_column("status", String(12), nullable=True)
    category_id: Mapped[UUID | None] = mapped_column(
        "category_id", Uuid, ForeignKey("Category.id"), default=None, nullable=True
    )
    series_id: Mapped[UUID | None] = mapped_column(
        "series_id", Uuid, ForeignKey("Series.id"), default=None, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.today()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    deleted_at: Mapped[datetime] = mapped_column("deleted_at", DateTime, nullable=True)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    series: Mapped["Series"] = relationship("Series", back_populates="products")
    tags: Mapped[List["Tag"]] = relationship(
        secondary=product_tag, back_populates="products"
    )
    thumbnail: Mapped[str] = mapped_column("thumbnail", String(255), nullable=True)
    variant: Mapped[str | None] = mapped_column("variant", Text(), nullable=True)
    preorder_start_date: Mapped[datetime | None] = mapped_column(
        "preorder_start_date", DateTime, nullable=True
    )
    preorder_end_date: Mapped[datetime | None] = mapped_column(
        "preorder_end_date", DateTime, nullable=True
    )

    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        original_price: float,
        sell_price: float,
        quantity: int,
        thumbnail: str,
        slug: str,
        country: str,
        factory: str,
        status: str,
        series_id: UUID | None = None,
        category_id: UUID | None = None,
        variant: str | None = None,
        preorder_start_date: datetime | None = None,
        preorder_end_date: datetime | None = None,
    ):
        print("Product model")
        self.id = id
        self.name = name
        self.description = description
        self.original_price = original_price
        self.sell_price = sell_price
        self.quantity = quantity
        self.thumbnail = thumbnail
        self.series_id = series_id
        self.slug = slug
        self.country = country
        self.factory = factory
        self.status = status
        self.category_id = category_id
        self.created_at = datetime.today()
        self.variant = variant
        self.preorder_start_date = preorder_start_date
        self.preorder_end_date = preorder_end_date

    def __repr__(self):
        return f"<Product {self.name}>"


# CATEGORY TABLE
class Category(Base):
    """
    Category model
    """

    __tablename__ = "Category"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)
    slug: Mapped[str] = mapped_column("slug", String(50), unique=True, nullable=True)
    parent_id: Mapped[UUID] = mapped_column("parent_id", Uuid, nullable=True)
    description: Mapped[str] = mapped_column("description", Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.today()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="category"
    )
    deleted_at: Mapped[datetime] = mapped_column("deleted_at", DateTime, nullable=True)

    def __init__(
        self,
        id: UUID,
        name: str,
        parent_id: UUID | None,
        description: str,
        slug: str | None,
    ):
        print("Category model")
        if parent_id:
            self.parent_id = parent_id
        if slug:
            self.slug = slug
        self.id = id
        self.name = name
        self.description = description
        self.created_at = datetime.today()

    def __repr__(self):
        return f"<Category {self.name}>"

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "description": self.description,
        }


# TAG TABLE
class Tag(Base):
    """
    Tag model
    """

    __tablename__ = "Tag"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)

    products: Mapped[List["Product"]] = relationship(
        secondary=product_tag, back_populates="tags"
    )
    deleted_at: Mapped[datetime] = mapped_column("deleted_at", DateTime, nullable=True)

    def __init__(self, id: UUID, name: str):
        print("Tag model")
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Tag {self.name}>"


# DEPOSIT_TYPE TABLE
class DepositType(Base):
    """
    DepositType model
    """

    __tablename__ = "DepositType"

    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)
    value: Mapped[float] = mapped_column("value", Float)
    fee: Mapped[float] = mapped_column("fee", Float)
    bills: Mapped[List["Bill"]] = relationship("Bill", back_populates="deposit_type")
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.today()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)

    def __init__(self, id: UUID, name: str, value: float, fee: float):
        print("DepositType model")
        self.id = id
        self.name = name
        self.value = value
        self.fee = fee
        self.created_at = datetime.now()

    def __repr__(self):
        return f"<DepositType {self.name}>"


class Series(Base):
    """
    Series Model
    """

    __tablename__ = "Series"
    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)
    slug: Mapped[str] = mapped_column("slug", String(255), unique=True)
    description: Mapped[str] = mapped_column("description", Text(), nullable=True)
    image: Mapped[str] = mapped_column("image", String(255), nullable=True)
    products: Mapped[List["Product"]] = relationship("Product", back_populates="series")
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.today()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column("deleted_at", DateTime, nullable=True)

    def __init__(self, id: UUID, name: str, slug: str, description: str, image: str):
        self.id = id
        self.name = name
        self.slug = slug
        self.description = description
        self.image = image

    def __repr__(self):
        return f"<Series {self.name}>"


# PRODUCTS_IMAGE TABLE
class ProductsImage(Base):
    """
    ProductsImage Model
    """

    __tablename__ = "ProductsImage"
    id: Mapped[UUID] = mapped_column("id", Uuid, primary_key=True)
    slug: Mapped[str] = mapped_column("slug", String(255), unique=True)
    image_url: Mapped[str] = mapped_column("image_url", String(255), nullable=True)
    product_id: Mapped[UUID] = mapped_column(
        "product_id", Uuid, ForeignKey("Product.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=datetime.today()
    )
    updated_at: Mapped[datetime] = mapped_column("updated_at", DateTime, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column("deleted_at", DateTime, nullable=True)

    def __init__(self, id: UUID, slug: str, image_url: str, product_id: UUID):
        self.id = id
        self.slug = slug
        self.image_url = image_url
        self.product_id = product_id
        self.created_at = datetime.today()

    def __repr__(self):
        return f"<ProductsImage {self.id}>"
