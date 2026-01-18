from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


def create_db_engine(
    database_url: str,
    pool_size: int | None = None,
) -> AsyncEngine:
    engine = create_async_engine(
        database_url,
        pool_size=pool_size,
        max_overflow=0,
        pool_timeout=30,
    )

    return engine
