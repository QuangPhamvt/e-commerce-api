from fastapi import HTTPException, status
from app.database.crud import tag_crud
from app.utils.uuid import convert_str_to_uuid
from sqlalchemy.ext.asyncio import AsyncSession


class Delete:
    async def delete(self, id: str, db: AsyncSession):
        tag_id = convert_str_to_uuid(id)
        tag = await tag_crud.get_tag_by_id(tag_id, db)
        if not tag:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Tag not found!")
        await tag_crud.delete_tag(tag_id, db)
        return {"detail": "Delete Tag Succeed!"}
