from app.database.models import Bio
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.uuid import generate_uuid
from app.schemas.bio import CreateBioParam


async def create_bio(db: AsyncSession, user_data: CreateBioParam) -> Bio:
    bio_id = generate_uuid()
    db_bio = Bio(
        id=bio_id,
        user_id=user_data.user_id,
        username=user_data.username,
        fullname=user_data.fullname,
        phone_number=user_data.phone_number,
    )
    db.add(db_bio)
    await db.commit()
    await db.refresh(db_bio)
    return db_bio
