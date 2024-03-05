from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.database import Base

from .database import engine_local
from .routers import roles, auth
from .middlewares import db_session_middleware, log_middleware
from .configs.constants import DOCUMENTATIONS


app = FastAPI(**DOCUMENTATIONS)

origins = [
    "http://localhost:3000",
    "https:dev.customafk.com",
    "https:dev.admin.customafk.com",
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
app.include_router(roles.router)


@app.get("/")
async def read_root():
    return {"msg": "Hello World"}
