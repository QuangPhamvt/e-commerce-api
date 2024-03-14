from uuid import UUID
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(
        title="Name",
        description="Name of product",
        examples=["Iphone 13"],
    )
    description: str = Field(
        title="Description",
        description="Description of product",
        examples=["This is a new product from Apple"],
    )
    original_price: float = Field(
        title="Original Price",
        description="Original price of product",
        examples=[1000.0],
    )
    sell_price: float = Field(
        title="Sell Price",
        description="Sell price of product",
        examples=[900.0],
    )
    quantity: int = Field(
        title="Quantity",
        description="Quantity of product",
        examples=[100],
    )
    country: str = Field(
        title="Conutry",
        description="Conutry of product",
        examples=["USA"],
    )
    factory: str = Field(
        title="Factory",
        description="Factory of product",
        examples=["Apple"],
    )
    status: str = Field(
        title="Status",
        description="Status of product",
        examples=["active"],
    )
    pass


class ResGetProducts:
    id: UUID = Field(
        title="ID",
        description="ID of product",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    name: str = Field(
        title="Name",
        description="Name of product",
        examples=["Iphone 13"],
    )
    slug: str = Field(
        title="Slug",
        description="Slug of product",
        examples=["iphone-13"],
    )
    image: str = Field(
        title="Image",
        description="Image of product",
        examples=["https://example.com/image.jpg"],
    )
    sell_price: float = Field(
        title="Sell Price",
        description="Sell price of product",
        examples=[900.0],
    )
    quantity: int = Field(
        title="Quantity",
        description="Quantity of product",
        examples=[100],
    )
    conutry: str = Field(
        title="Conutry",
        description="Conutry of product",
        examples=["USA"],
    )
    factory: str = Field(
        title="Factory",
        description="Factory of product",
        examples=["Apple"],
    )
    status: str = Field(
        title="Status",
        description="Status of product",
        examples=["active"],
    )
    pass


class ProductCreateCRUD(ProductBase):
    image: str = Field(
        title="Image",
        description="Image of product",
        examples=["https://example.com/image.jpg"],
    )
    pass


class BodyCreateProduct(ProductBase):
    pass


class ResCreateProduct(BaseModel):
    detail: str = Field(
        title="Detail",
        description="Detail of product",
        examples=["Product created successfully"],
    )
    presigned_url: str = Field(
        title="Presigned URL",
        description="Presigned URL of product",
        examples=["https://example.com/image.jpg"],
    )


class BodyUpdateProduct(BaseModel):
    name: str | None = Field(
        title="Name",
        description="Name of product",
        examples=["Iphone 13"],
        default=None,
    )
    slug: str | None = Field(
        title="Slug",
        description="Slug of product",
        examples=["iphone-13"],
        default=None,
    )
    description: str | None = Field(
        title="Description",
        description="Description of product",
        examples=["This is a new product from Apple"],
        default=None,
    )
    sell_price: float | None = Field(
        title="Sell Price",
        description="Sell price of product",
        examples=[900.0],
        default=None,
    )
    original_price: float | None = Field(
        title="Original Price",
        description="Original price of product",
        examples=[1000.0],
        default=None,
    )
    country: str | None = Field(
        title="Conutry",
        description="Conutry of product",
        examples=["USA"],
        default=None,
    )
    factory: str | None = Field(
        title="Factory",
        description="Factory of product",
        examples=["Apple"],
        default=None,
    )
    status: str | None = Field(
        title="Status",
        description="Status of product",
        examples=["active"],
        default=None,
    )
    pass
