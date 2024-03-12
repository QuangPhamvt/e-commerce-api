from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str


class CreateCategoryParam(CategoryBase):
    slug: str | None = None


class UpdateCategoryParam(CreateCategoryParam):
    pass
