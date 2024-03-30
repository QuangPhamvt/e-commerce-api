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


class CreateSeriesBody(SeriesBase):
    image_type: str = Field(
        title="Image Type",
        description="Image type of series",
        examples=["jpeg"],
    )
    pass


class UpdateSeriesParam(SeriesBase):
    pass


class UpdateSeriesById(SeriesBase):
    slug: str = Field(
        title="Series Slug",
        description="Series Slug",
        examples=["series-1"],
    )


class CreateSeriesCRUD(SeriesBase):
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


class ListSeriesResponse(CreateSeriesBody):
    id: str = Field(
        title="ID",
        description="ID of series",
        examples=["194bd139744847ba8c151e55e93a6a5c"],
    )
