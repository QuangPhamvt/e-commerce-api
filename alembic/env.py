from logging.config import fileConfig
from dotenv import dotenv_values

from sqlalchemy import create_engine
from alembic import context
from app.database import Base
# from app.database.models import User


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    Config = dotenv_values(".env")

    url_tokens = {
        "DB_USERNAME": Config.get("DB_USERNAME", ""),
        "DB_PASSWORD": Config.get("DB_PASSWORD", ""),
        "DB_HOST": Config.get("DB_HOST", ""),
        "DB_NAME": Config.get("DB_NAME", ""),
    }
    print(f"URL Tokens: {url_tokens['DB_HOST']}")

    url = config.get_main_option("sqlalchemy.url")

    if url is None:
        raise ValueError("sqlalchemy.url is not set")

    url = f"mysql+pymysql://{url_tokens['DB_USERNAME']}:{url_tokens['DB_PASSWORD']}@{url_tokens['DB_HOST']}:3306/{url_tokens['DB_NAME']}"

    connectable = create_engine(url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
