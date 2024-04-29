from uuid import UUID
from pydantic import BaseModel, Field
from enum import Enum


class StatusEnum(str, Enum):
    # Bill was canceled
    CANCELED = ("CANCELED",)
    # Bill is waiting for payment
    PENDING = ("PENDING",)
    # Bill is paid, being processed
    PROCESSING = "PROCESSING"
    # Bill is completed
    COMPLETED = "COMPLETED"


class CreateBillDetailBody(BaseModel):
    quantity: int = Field(
        title="Quantity",
        description="Quantity of product",
        examples=[
            1,
        ],
    )
    price: float = Field(
        title="Price",
        description="Price of product",
        examples=[
            5000,
        ],
        default=None,
    )
    product_id: UUID = Field(
        title="Product id",
        description="Product id",
        examples=[
            "123e4567e89b12d3a456426614174000",
        ],
    )


class CreateBillBody(BaseModel):
    deposit_type_id: UUID | None = Field(
        title="Deposit type id",
        description="Deposit type id",
        examples=[
            "123e4567e89b12d3a456426614174000",
        ],
        default=None,
    )
    deposit_type_id: UUID | None = Field(
        title="Deposit type id",
        description="Deposit type id",
        examples=[
            "123e4567e89b12d3a456426614174000",
        ],
        default=None,
    )
    customer_province: str = Field(
        title="Province",
        description="Province of customer",
        examples=[
            "Ho Chi Minh",
        ],
        default=None,
    )

    customer_district: str = Field(
        title="District",
        description="District of customer",
        examples=[
            "District 1",
        ],
        default=None,
    )
    customer_ward: str = Field(
        title="Ward",
        description="Ward of customer",
        examples=[
            "Da Kao Ward ",
        ],
        default=None,
    )
    customer_address: str = Field(
        title="Address",
        description="Address of customer",
        examples=[
            "123 Nguyen Dinh Chieu",
        ],
        default=None,
    )
    customer_fullname: str = Field(
        title="Fullname",
        description="Fullname of customer",
        examples=[
            "Nakiri Ayame",
        ],
        default=None,
    )
    customer_phone_number: str = Field(
        title="Phone number",
        description="Phone number of customer",
        examples=[
            "0123456789",
        ],
        default=None,
    )
    product_price: float = Field(
        title="Product price",
        description="Product price",
        examples=[
            5000,
        ],
        default=None,
    )
    details: list[CreateBillDetailBody]


class CreateBillData(BaseModel):
    user_id: UUID
    customer_province: str
    customer_district: str
    customer_ward: str
    customer_address: str
    customer_address: str
    customer_fullname: str
    customer_phone_number: str
    product_price: float
    deposit_type_id: UUID | None = None
    status: StatusEnum


class CreateBillDetailData(CreateBillDetailBody):
    bill_id: UUID


class ProductBillInfo(BaseModel):
    id: UUID
    name: str
    quantity: int
