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
    pass


class UpdateCategoryParam(CreateCategoryParam):
    pass


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
