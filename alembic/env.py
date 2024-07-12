from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os

# Load environment variables from .env file
dotenv_path = '/Users/denissergeich/service/pythonProject/mlservice/app/.env'
load_dotenv(dotenv_path)

# This line sets up loggers basically.
config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

# Import all your SQLAlchemy models here that need to be included in migrations
# Make sure to import them from the correct module path
from app.models.user import User
from app.models.request import Request
from app.database.database import Base, engine
from app.models.balance import Balance

# Attach the metadata of your Base class (which includes all SQLAlchemy models)
# This is crucial for 'autogenerate' support
target_metadata = Base.metadata

# This function is used when running migrations without a live database connection.
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# This function runs migrations with a live database connection.
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether to run migrations offline or online based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

