from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from app.configs.constants import ProductStatus


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
        examples=[ProductStatus.in_stock],
    )
    slug: str = Field(
        title="Slug",
        description="Slug of Product",
        examples=["category-1"],
    )
    pass


class ProductCreateCRUD(ProductBase):
    images: str = Field(
        title="Image",
        description="Image of product",
        examples=["example.com/image1.jpg,example.com/image2.jpg,"],
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


class CreateProductResponse(ProductBase):
    images: str = Field(
        title="Image",
        description="Image of product",
        examples=["example.com/image1.jpg,example.com/image2.jpg,"],
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
    preorder_start_date: datetime | None = Field(
        title="Preorder Start Date",
        description="Preorder Start Date of product",
        examples=[datetime.now()],
    )
    preorder_end_date: datetime | None = Field(
        title="Preorder End Date",
        description="Preorder End Date of product",
        examples=[datetime.now()],
    )


class BodyUpdateProduct(CreateProductResponse):
    deleted_at: datetime | None = Field(
        title="Deleted At",
        description="Product is out of stock",
        examples=[datetime.now()],
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
