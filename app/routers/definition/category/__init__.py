from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.configs.constants import CATEGORY, CATEGORY_PREFIX
from app.dependencies import get_db
from app.schemas.category import ListCategoryRespone
from app.services.category import CategoryService


router = APIRouter(prefix=CATEGORY_PREFIX, tags=[CATEGORY])


@router.get(
    "/",
    description="This endpoint is used to get list of category",
    status_code=status.HTTP_200_OK,
    response_model=list[ListCategoryRespone],
    responses={
        "200": {
            "description": "Get List Categories Succeed!",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Action Figures",
                            "description": "Action Figure description.",
                            "slug": "action-figures",
                            "id": "123e4567e89b12d3a456426614174000",
                        },
                        {
                            "name": "Truyện Tranh",
                            "description": "Truyen tranh description",
                            "slug": "truyen-tranh",
                            "id": "123e4567e89b12d3a456426614174000",
                        },
                    ]
                },
            },
        },
    },
)
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryService().get_all(db=db)
