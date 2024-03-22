from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.dependencies import get_current_username
from app.configs.documentations import DEFINITION_DOCUMENTATIONS

from .category import router as category_router
from .product import router as product_router
from .series import router as series_router
from .tag import router as tag_router


# Definition Api
definition_api = FastAPI(docs_url=None, **DEFINITION_DOCUMENTATIONS)

definition_api.include_router(category_router)
definition_api.include_router(product_router)
definition_api.include_router(series_router)
definition_api.include_router(tag_router)


@definition_api.get("/")
def read_def():
    return {"message": "Hello World from definition api"}


@definition_api.get("/docs", include_in_schema=False)
async def get_swagger_def_documentation(
    __username__: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/def/openapi.json",
        title="E-commerce API Documentation",
    )


@definition_api.get("/openapi.json", include_in_schema=False)
async def def_openapi(__username__: str = Depends(get_current_username)):
    get_openapi(
        title=definition_api.title,
        version=definition_api.version,
        routes=definition_api.routes,
    )
