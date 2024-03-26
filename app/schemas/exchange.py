from pydantic import BaseModel, Field


class ExchangeBase(BaseModel):
    currency: str = Field(
        title="Currency",
        description="Currency of exchange rate",
        examples=["USD"],
    )
    rate: float = Field(
        title="Rate",
        description="rate of currency",
        examples=[2.1],
    )


class CreateExchangeParams(ExchangeBase):
    pass


class CreateExchangeData(ExchangeBase):
    pass


class UpdateExchangeParams(ExchangeBase):
    pass


class UpdateExchangeData(ExchangeBase):
    pass


class ExchangeResponse(ExchangeBase):
    pass


class ResCreateExchange(BaseModel):
    detail: str = Field(
        title="Detail",
        description="Detail of response",
        examples=["Create Exchange Succeed!"],
    )
