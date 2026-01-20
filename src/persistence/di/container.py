from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from core.services import OrganizationsService
from persistence.db.repositories import OrganizationsRepositoryImpl
from config.settings import settings


class Container(containers.DeclarativeContainer):
    db_engine = engine = create_async_engine(
        settings.database_url,
        pool_size=settings.db_pool_size,
        max_overflow=0,
        pool_timeout=30,
    )
    db_session = sessionmaker(
        db_engine,
        class_=AsyncSession,
    )
    organizations_repository = providers.Factory(
        OrganizationsRepositoryImpl,
        session=db_session,
    )
    organizations_service = providers.Factory(OrganizationsService, organizations_repository=organizations_repository)
