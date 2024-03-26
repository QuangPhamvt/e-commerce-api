from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import tag_crud, product_tag_crud
from app.schemas.tag import TagBase
from app.utils.helper import helper


class AddProductTag:
    async def add(self, id: str, tags: list[TagBase], db: AsyncSession):
        product_id = helper.convert_str_to_UUID(id)
        for tag in tags:
            tag_id = await tag_crud.is_exist_name(tag.name, db)
            if not tag_id:
                await tag_crud.create(tag, db)
                tag_id = await tag_crud.is_exist_name(tag.name, db)
            is_relation_exist = await product_tag_crud.is_exist_product_tag(
                product_id, tag_id, db
            )
            if not is_relation_exist:
                await product_tag_crud.create(product_id, tag_id, db)
        return {"detail": "Add Tags For Product Succeed!"}
