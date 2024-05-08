from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.dependencies import get_current_username
from app.configs.documentations import USER_DOCUMENTATIONS
from .cart import router as cart_router
from .payment import router as payment_router

# Website Api
web_api = FastAPI(docs_url=None, **USER_DOCUMENTATIONS)
web_api.include_router(cart_router)
web_api.include_router(payment_router)


@web_api.get("")
def read_website():
    return {"message": "Hello World from web api"}


@web_api.get("/docs", include_in_schema=False)
async def get_swagger_website_documentation(
    __username__: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/web/openapi.json",
        title="E-commerce API Documentation",
    )


@web_api.get("/openapi.json", include_in_schema=False)
async def web_openapi(__username__: str = Depends(get_current_username)):
    get_openapi(title=web_api.title, version=web_api.version, routes=web_api.routes)
