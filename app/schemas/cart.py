from uuid import UUID
from pydantic import BaseModel, Field


class CartBase(BaseModel):
    product_id: UUID = Field(
        title="Product Id",
        description="Product Id",
        examples=[
            "123e4567e89b12d3a456426614174000",
        ],
        default=None,
    )
    quantity: int = Field(
        title="Quantity",
        description="Quantity of product",
        examples=[
            1,
        ],
    )


class CreateCartParam(CartBase):
    pass


class CreateCartData(CartBase):
    user_id: UUID
