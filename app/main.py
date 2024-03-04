from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.database import Base

from .database import engine_local
from .routers import items, users, roles
from .routers import auth
from .middlewares import db_session_middleware, log_middleware

from .configs.constants import DOCUMENTATIONS


app = FastAPI(**DOCUMENTATIONS)


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


app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)
app.include_router(roles.router)


@app.get("/")
async def read_root():
    return {"msg": "Hello World"}
