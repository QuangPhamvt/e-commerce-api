from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config, command
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.configs.constants import ROOT_PATH

from app.database import Base, engine_local
from app.middlewares import db_session_middleware, log_middleware

from .routers.auth import auth_api
from .routers.admin import admin_api
from .routers.website import web_api
from .routers.definition import definition_api

log = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(__app__: FastAPI):
    log.info("Starting up...")
    log.info("Running migrations...")
    alembic_cfg = Config("alembic.ini")
    exist_revision = command.history(alembic_cfg)
    if exist_revision:
        command.upgrade(alembic_cfg, "head")

    log.info("Creating tables...")
    async with engine_local.begin() as connection:
        # turn on to reset the database
        # await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield

    log.info("Shutting down...")


# app = FastAPI()
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://lunas-local.com:3000",
    "http://admin.lunas-local.com:3000",
    "https://dev.customafk.com",
    "https://dev.admin.customafk.com",
]


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


@app.get("/")
async def read_root():
    return {
        "msg": "Hello World",
        "website_docs": "https://dev.api.customafk.com/api/v1/web/docs",
        "admin_docs": "https://dev.api.customafk.com/api/v1/admin/docs",
        "auth_docs": "https://dev.api.customafk.com/api/v1/auth/docs",
        "def_docs": "https://dev.api.customafk.com/api/v1/def/docs",
    }


app.mount(f"{ROOT_PATH}/web", web_api)
app.mount(f"{ROOT_PATH}/admin", admin_api)
app.mount(f"{ROOT_PATH}/auth", auth_api)
app.mount(f"{ROOT_PATH}/def", definition_api)
