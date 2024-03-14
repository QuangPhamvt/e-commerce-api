from app.database.models import Bio
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.uuid import generate_uuid
from app.schemas.bio import CreateBioParam


async def create_bio(db: AsyncSession, user_data: CreateBioParam):
    bio_id = generate_uuid()
    if user_data.phone_number is None:
        user_data.phone_number = ""
    db_bio = Bio(id=bio_id, **user_data.model_dump())
    db.add(db_bio)
    await db.commit()
