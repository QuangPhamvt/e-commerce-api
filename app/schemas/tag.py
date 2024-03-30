from uuid import UUID
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(
        title="Tag Name",
        description="Tag name",
        examples=["Tag 1"],
    )


class CreateTagParam(TagBase):
    pass


class UpdateTagParam(TagBase):
    pass


class CreateTagData(TagBase):
    pass


class UpdateTagData(TagBase):
    pass


class ListTagRespone(TagBase):
    id: str = Field(
        title="Tag ID",
        description="ID of Tag",
        examples=["7625f01998634bfcad8301cfa07495b5"],
    )


class UpdateProductTagParam(BaseModel):
    tags: list[TagBase] = Field(
        title="Tag ID",
        description="Tag ID",
        examples=[[{"name": "Tag 1"}]],
    )

    product_id: UUID = Field(
        title="Product ID",
        description="Product ID",
        examples=["7625f01998634bfcad8301cfa07495b5"],
    )


class ListTagRequest(ListTagRespone):
    pass
