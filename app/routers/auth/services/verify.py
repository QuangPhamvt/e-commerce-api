from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import user_crud
from app.schemas.auth import VerifyPayload


class Verify:
    @staticmethod
    async def verify(payload: VerifyPayload, db: AsyncSession):
        print(f"from service: ${payload}")
        await user_crud.verify_user(db=db, payload=payload)
        return {"message": "Verify Succeed!"}
