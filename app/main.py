from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.database import Base
from app.dependencies import get_current_username
from .database import engine_local
from .middlewares import db_session_middleware, log_middleware
from .configs.documentations import (
    ADMIN_DOCUMENTATIONS,
    AUTH_DOCUMENTATIONS,
    DEFINITION_DOCUMENTATIONS,
    USER_DOCUMENTATIONS,
)
from .routers.v1.admin import router as admin_router
from .routers.v1.auth import router as auth_router
from .routers.v1.definition import router as definition_router
from .routers.v1.user import router as user_router

app = FastAPI(docs_url=None, **USER_DOCUMENTATIONS)

origins = [
    "http://localhost:3000",
    "http://lunas-local.com:3000",
    "http://admin.lunas-local.com:3000",
    "https://dev.customafk.com",
    "https://dev.admin.customafk.com",
]


@app.on_event("startup")
async def init_models():
    print("starting server")
    async with engine_local.begin() as connection:
        # turn on to reset the database
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


app.add_middleware(BaseHTTPMiddleware, dispatch=db_session_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)


@app.get("/")
async def read_root():
    return {"msg": "Hello World"}


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="E-commerce API Documentation"
    )


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    get_openapi(title=app.title, version=app.version, routes=app.routes)


# Admin Api
admin_api = FastAPI(docs_url=None, **ADMIN_DOCUMENTATIONS)

admin_api.include_router(admin_router)


@admin_api.get("/")
def read_admin():
    return {"message": "Hello World from admin api"}


@admin_api.get("/docs", include_in_schema=False)
async def get_swagger_admin_documentation(
    username: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/admin-api/openapi.json",
        title="E-commerce API Documentation",
    )


@admin_api.get("/openapi.json", include_in_schema=False)
async def admin_openapi(username: str = Depends(get_current_username)):
    get_openapi(
        title=admin_api.title, version=admin_api.version, routes=admin_api.routes
    )


# Auth Api
auth_api = FastAPI(docs_url=None, **AUTH_DOCUMENTATIONS)

auth_api.include_router(auth_router)


@auth_api.get("/")
def read_auth():
    return {"message": "Hello World from auth api"}


@auth_api.get("/docs", include_in_schema=False)
async def get_swagger_auth_documentation(
    username: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/auth-api/openapi.json",
        title="E-commerce API Documentation",
    )


@auth_api.get("/openapi.json", include_in_schema=False)
async def auth_openapi(username: str = Depends(get_current_username)):
    get_openapi(title=auth_api.title, version=auth_api.version, routes=auth_api.routes)


# Definition Api
definition_api = FastAPI(docs_url=None, **DEFINITION_DOCUMENTATIONS)

definition_api.include_router(definition_router)


@definition_api.get("/")
def read_def():
    return {"message": "Hello World from definition api"}


@definition_api.get("/docs", include_in_schema=False)
async def get_swagger_def_documentation(
    username: str = Depends(get_current_username),
):
    return get_swagger_ui_html(
        openapi_url="/api/v1/def-api/openapi.json",
        title="E-commerce API Documentation",
    )


@definition_api.get("/openapi.json", include_in_schema=False)
async def def_openapi(username: str = Depends(get_current_username)):
    get_openapi(
        title=definition_api.title,
        version=definition_api.version,
        routes=definition_api.routes,
    )


app.mount("/admin-api", admin_api)
app.mount("/auth-api", auth_api)
app.mount("/def-api", definition_api)
