from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.database import Base
from app.dependencies import get_current_username

from .database import engine_local
from .routers import role, auth, user, category, product, series, tag
from .middlewares import db_session_middleware, log_middleware
from .configs.constants import DOCUMENTATIONS


app = FastAPI(docs_url=None, **DOCUMENTATIONS)

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


app.include_router(auth.router)
app.include_router(role.router)
app.include_router(tag.router)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(series.router)


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
