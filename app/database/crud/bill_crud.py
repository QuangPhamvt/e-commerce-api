from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Bill, BillDetail
from app.schemas.bill import CreateBillData, CreateBillDetailData, StatusEnum
from app.utils.uuid import generate_uuid


class BillCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_bill(self, data: CreateBillData, bill_id: UUID, payos_id: int):
        db_bill = Bill(id=bill_id, payos_id=payos_id, **data.model_dump())
        self.db.add(db_bill)
        await self.db.commit()
        return

    async def create_bill_detail(self, data: CreateBillDetailData):
        id = generate_uuid()
        db_bill_detail = BillDetail(id=id, **data.model_dump())
        self.db.add(db_bill_detail)
        await self.db.commit()
        return

    async def update_bill_status_by_order_code(
        self, order_code: int, status: StatusEnum
    ):
        await self.db.execute(
            update(Bill).where(Bill.payos_id == order_code).values(status=status)
        )
        await self.db.commit()
        return

    async def read_by_order_code(self, order_code: int):
        return (
            (await self.db.execute(select(Bill).where(Bill.payos_id == order_code)))
            .scalars()
            .first()
        )
