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
    image: str = Field(
        title="Image",
        description="Image of product",
        examples=[
            "https://www.apple.com/newsroom/images/product/iphone/standard/Apple_iphone13-pro-max-iphone13-pro-iphone13-hero-2021.jpg.large.jpg"
        ],
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


class ProductCreate(ProductBase):
    pass
