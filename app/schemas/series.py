from pydantic import BaseModel, Field


class SeriesBase(BaseModel):
    name: str = Field(
        title="Series Name",
        description="Series name",
        examples=["Series 1"],
    )
    description: str = Field(
        title="Series Description",
        description="Series description",
        examples=["Series 1 description"],
    )


class CreateSeriesParam(SeriesBase):
    pass


class UpdateSeriesParam(SeriesBase):
    pass


class UpdateSeriesData(SeriesBase):
    slug: str = Field(
        title="Series Slug",
        description="Series Slug",
        examples=["series-1"],
    )


class CreateSeriesData(SeriesBase):
    image: str = Field(
        title="Series Image",
        description="Series Image",
        examples=["https://example.com/image.jpg"],
    )
    slug: str = Field(
        title="Series Slug",
        description="Series Slug",
        examples=["series-1"],
    )


class CreateSeriesResponse(BaseModel):
    detail: str = Field(
        title="Detail",
        description="Detail of series",
        examples=["Product created successfully"],
    )
    presigned_url: str = Field(
        title="Presigned URL",
        description="Presigned URL of product",
        examples=["https://example.com/image.jpg"],
    )


class ListSeriesResponse(CreateSeriesData):
    id: str = Field(
        title="ID",
        description="ID of series",
        examples=["194bd139744847ba8c151e55e93a6a5c"],
    )
