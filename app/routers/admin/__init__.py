from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app.dependencies import get_current_username
from app.configs.documentations import ADMIN_DOCUMENTATIONS

from .category import router as category_router
from .product import router as product_router
from .series import router as series_router
from .tag import router as tag_router
from .role import router as role_router
from .deposit import router as deposit_router
from .exchange import router as exchange_router
from .user import router as user_router

# Admin Api
admin_api = FastAPI(docs_url=None, **ADMIN_DOCUMENTATIONS)

admin_api.include_router(category_router)
admin_api.include_router(product_router)
admin_api.include_router(series_router)
admin_api.include_router(tag_router)
admin_api.include_router(role_router)
admin_api.include_router(deposit_router)
admin_api.include_router(exchange_router)
admin_api.include_router(user_router)


@admin_api.get("/")
def read_admin():
    return {"message": "Hello World from admin api"}


@admin_api.get("/docs", include_in_schema=False)
async def get_swagger_admin_documentation(
    __username__: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/admin/openapi.json",
        title="E-commerce API Documentation",
    )


@admin_api.get("/openapi.json", include_in_schema=False)
async def admin_openapi(__username__: str = Depends(get_current_username)):
    return get_openapi(
        title=admin_api.title, version=admin_api.version, routes=admin_api.routes
    )
