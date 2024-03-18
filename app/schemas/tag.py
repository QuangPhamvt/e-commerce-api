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
