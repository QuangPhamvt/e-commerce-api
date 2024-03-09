from sqlalchemy import URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
from dotenv import dotenv_values
from app.configs.constants import DB_PORT

config = dotenv_values(".env")

# check type in python is number
url_create = URL.create(
    drivername="mysql+asyncmy",
    username=config["DB_USERNAME"],
    password=config["DB_PASSWORD"],
    host=config["DB_HOST"],
    port=DB_PORT,
    database=config["DB_NAME"],
)

engine_local = create_async_engine(
    url_create,
    echo=True,
    pool_size=50,
    max_overflow=10,
)
SessionLocal = async_sessionmaker(
    bind=engine_local,
    autocommit=False,
    autoflush=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    pass
