import sys
import asyncio
from pathlib import Path
from os.path import dirname, abspath
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

# ⚠️ ВАЖНО: Добавляем путь ДО импортов из app

sys.path.insert(0, dirname(dirname(abspath(__file__))))

# Теперь импортируем из app
from app.core.config import settings
from app.core.database import Base
from app.users.models import User

config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Устанавливаем URL базы данных
config.set_main_option("sqlalchemy.url", settings.get_database_url())

# Метаданные для автогенерации миграций
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Выполняет миграции синхронно через connection."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode with async."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.begin() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


# Выбираем режим и запускаем миграции
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())