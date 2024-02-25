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

print(url_create)
engine_local = create_async_engine(url_create)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine_local)


class Base(AsyncAttrs, DeclarativeBase):
    pass
