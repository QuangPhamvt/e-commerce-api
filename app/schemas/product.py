from typing import Sequence
from uuid import UUID
from pydantic import BaseModel, Field
import datetime
from app.configs.constants import ProductStatus
from enum import Enum


class OrderNumber(str, Enum):
    ONE = "one"
    TWO = "two"
    THREE = "three"
    FOUR = "four"
    FIVE = "five"


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
    status: ProductStatus = Field(
        title="Status",
        description="Status of product",
        examples=[ProductStatus.IN_STOCK],
    )
    slug: str = Field(
        title="Slug",
        description="Slug of Product",
        examples=["iphone-13"],
    )
    pass


class ProductCreateCRUD(ProductBase):
    thumbnail: str = Field(
        title="Thumbnail",
        description="Images of product",
        examples=["example.com/image1.jpg,example.com/image2.jpg,"],
    )
    pass


class BodyCreateProduct(ProductBase):
    thumbnail_type: str = Field(
        title="Thumbnail Type",
        description="Type of thumbnail",
        examples=["jpeg"],
    )
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


class CreateProductResponse(ProductBase):
    thumbnail: str | None = Field(
        title="Thumbnail",
        description="Thumbnail of product",
        examples=["example.com/thumbnail.jpg"],
    )
    variant: str | None = Field(
        title="Variant",
        description="Variant of product",
        examples=["[{type:string,size:string},]"],
    )
    preorder_start_date: str | None = Field(
        title="Preorder Start Date",
        description="Preorder Start Date of product",
        examples=[datetime.datetime.now()],
    )
    preorder_end_date: str | None = Field(
        title="Preorder End Date",
        description="Preorder End Date of product",
        examples=[datetime.datetime.now()],
    )


class BodyUpdateProduct(BaseModel):
    name: str = Field(
        title="Name",
        description="Name of product",
        examples=["Iphone 13"],
        default=None,
    )
    description: str = Field(
        title="Description",
        description="Description of product",
        examples=["This is a new product from Apple"],
        default=None,
    )
    original_price: float = Field(
        title="Original Price",
        description="Original price of product",
        examples=[1000.0],
        default=None,
    )
    sell_price: float = Field(
        title="Sell Price",
        description="Sell price of product",
        examples=[900.0],
        default=None,
    )
    quantity: int = Field(
        title="Quantity",
        description="Quantity of product",
        examples=[100],
        default=None,
    )
    country: str = Field(
        title="Conutry",
        description="Conutry of product",
        examples=["USA"],
        default=None,
    )
    factory: str = Field(
        title="Factory",
        description="Factory of product",
        examples=["Apple"],
        default=None,
    )
    status: ProductStatus = Field(
        title="Status",
        description="Status of product",
        examples=[ProductStatus.IN_STOCK],
        default=None,
    )
    thumbnail: str | None = Field(
        title="Thumbnail",
        description="Thumbnail of product",
        examples=["example.com/thumbnail.jpg"],
        default=None,
    )
    variant: str | None = Field(
        title="Variant",
        description="Variant of product",
        examples=["[{type:string,size:string},]"],
        default=None,
    )
    preorder_start_date: str | None = Field(
        title="Preorder Start Date",
        description="Preorder Start Date of product",
        examples=[datetime.datetime.now()],
        default=None,
    )
    preorder_end_date: str | None = Field(
        title="Preorder End Date",
        description="Preorder End Date of product",
        examples=[datetime.datetime.now()],
        default=None,
    )

    deleted_at: str | None = Field(
        title="Deleted At",
        description="Product is out of stock",
        examples=[datetime.datetime.now()],
        default=None,
    )


class GetListProduct(BodyUpdateProduct):
    id: UUID = Field(
        title="ID",
        description="ID of product",
        examples=["adf6377b-1151-4206-951f-1301f926078a"],
    )
    series_id: UUID | None = Field(
        title="Series ID",
        description="ID of series",
        examples=["194bd139-7448-47ba-8c15-1e55e93a6a5c"],
    )
    category_id: UUID | None = Field(
        title="Category ID",
        description="ID of category",
        examples=["123e4567-e89b-12d3-a456-426614174000"],
    )
    sell_price: float = Field(
        exclude=True,
        title="Sell Price",
        description="Sell price of product",
        examples=[900.0],
    )


class GetProductById(ProductBase):
    tags: Sequence = Field(
        title="Tags",
        description="Tags of product",
        examples=["[{id:UUID,name:string},]"],
    )
    thumbnail: str | None = Field(
        title="Thumbnail",
        description="Thumbnail of product",
        examples=["example.com/thumbnail.jpg"],
    )
    variant: str | None = Field(
        title="Variant",
        description="Variant of product",
        examples=["[{type:string,size:string},]"],
    )
    preorder_start_date: str | None = Field(
        title="Preorder Start Date",
        description="Preorder Start Date of product",
        examples=[datetime.datetime.now()],
    )
    preorder_end_date: str | None = Field(
        title="Preorder End Date",
        description="Preorder End Date of product",
        examples=[datetime.datetime.now()],
    )


class ImageType(BaseModel):
    type: str = Field(
        title="Image Type",
        description="type of image",
        examples=["png"],
    )
    order: OrderNumber = Field(
        title="Image Order Number",
        description="order of image",
        examples=["one"],
    )


class CreateProductsImageBody(BaseModel):
    slug: str = Field(
        title="Slug",
        description="Slug of product",
        examples=["iphone-13"],
    )
    image_url: str = Field(
        title="Image URL",
        description="URL of image",
        examples=["products/abc-one.jpg"],
    )
    product_id: UUID = Field(
        title="Product ID",
        description="ID of product",
        examples=["adf6377b-1151-4206-951f-1301f926078a"],
    )
