from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import tag_crud, product_tag_crud
from app.schemas.tag import CreateTagData
from app.utils.helper import helper


class AddProductTag:
    async def add(self, id: str, tags: list[str], db: AsyncSession):
        product_id = helper.convert_str_to_UUID(id)
        for tag in tags:
            tag_id = await tag_crud.is_exist_name(tag, db)
            if not tag_id:
                new_tag = CreateTagData(name=tag)
                await tag_crud.create(new_tag, db)
                tag_id = await tag_crud.is_exist_name(tag, db)
            is_relation_exist = await product_tag_crud.is_exist_product_tag(
                product_id, tag_id, db
            )
            if not is_relation_exist:
                await product_tag_crud.create(product_id, tag_id, db)
        return {"detail": "Add Tags For Product Succeed!"}
