from pydantic import BaseModel, Field


class DepositBase(BaseModel):
    name: str = Field(
        title="Name",
        description="Name of deposit",
        examples=["Deposit 70%"],
    )
    value: float = Field(
        title="Value",
        description="Value of deposit",
        examples=[0.7],
    )
    fee: float = Field(
        title="Fee",
        description="Fee of deposit",
        examples=[0.01],
    )


class CreateDepositParams(DepositBase):
    pass


class CreateDepositData(DepositBase):
    pass


class UpdateDepositParams(DepositBase):
    pass


class UpdateDepositData(DepositBase):
    pass


class DepositResponse(DepositBase):
    pass


class ResCreateDeposit(BaseModel):
    detail: str = Field(
        title="Detail",
        description="Detail of response",
        examples=["Create Deposit Succeed!"],
    )
