from uuid import UUID
from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(
        title="Category Name",
        description="Category name",
        examples=["Category 1"],
    )
    description: str = Field(
        title="Category Description",
        description="Category description",
        examples=["Category 1 description"],
    )


class CreateCategoryParam(CategoryBase):
    parent_id: UUID | None = Field(
        title="Parent ID",
        description="Parent ID of category",
        examples=["123e4567e89b12d3a456426614174000"],
        default=None,
    )
    pass


class UpdateCategoryParam(CreateCategoryParam):
    sub_id: list[UUID] | None = Field(
        title="Sub ID",
        description="Sub ID of category",
        examples=[
            "123e4567e89b12d3a456426614174000",
            "123e4567e89b12d3a456426614174001",
        ],
        default=None,
    )


class UpdateCategoryData(CategoryBase):
    parent_id: UUID | None = Field(
        title="Parent ID",
        description="Parent ID of category",
        examples=["123e4567e89b12d3a456426614174000"],
        default=None,
    )


class UpdateProductCategoryParam(BaseModel):
    category_id: UUID = Field(
        title="Category ID",
        description="Category ID",
        examples=["123e4567e89b12d3a456426614174000"],
    )
    product_id: UUID = Field(
        title="Product ID",
        description="Product ID",
        examples=["123e4567e89b12d3a456426614174000"],
    )


class ListCategoryRespone(CategoryBase):
    slug: str = Field(
        title="Slug",
        description="Slug of category",
        examples=["category-1"],
    )
    id: str = Field(
        title="ID",
        description="ID of category",
        examples=["123e4567e89b12d3a456426614174000"],
    )
