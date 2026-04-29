from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

def get_database_usrl() -> str:
    """
    Формирование URL подключения к базе данных SQLite.
    Args: -
    Return:
        str: URL для подключения к SQLite с поддержкой асинхронного драйвера aiosqlite
    """
    return f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"

engine = create_async_engine(
    get_database_usrl(),
    echo=True,
    pool_size=5,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
