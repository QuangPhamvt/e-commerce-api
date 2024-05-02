from pydantic import BaseModel


class ProductData(BaseModel):
    name: str
    quantity: int
    price: int


class BillData(BaseModel):
    # Dung hoi vi sao t dat ten nhu the nay, thang payos no bat the
    orderCode: int
    amount: int
    description: str
    buyerName: str
    buyerEmail: str
    buyerPhone: str
    buyerAddress: str


class PayloadData(BillData):
    items: list[ProductData]
    cancelUrl: str
    returnUrl: str
