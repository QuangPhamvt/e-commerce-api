from app.database.models import Bio
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.uuid import generate_uuid
from app.schemas.bio import CreateBioParam


class BioCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_bio(self, user_data: CreateBioParam):
        bio_id = generate_uuid()
        if user_data.phone_number is None:
            user_data.phone_number = ""
        db_bio = Bio(id=bio_id, **user_data.model_dump())
        self.db.add(db_bio)
        await self.db.commit()
