import os
from alembic import context
from alembic.config import Config
from sqlalchemy import create_engine, pool
from models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

target_metadata = None



def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    sqlalchemy_url = os.getenv("DATABASE_URL")

    config = Config()
    config.set_main_option('sqlalchemy.url', sqlalchemy_url)

    connectable = create_engine(
        sqlalchemy_url,
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata= Base.metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()