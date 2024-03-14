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
