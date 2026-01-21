from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from core.services import OrganizationService
from infrastructure.persistence.db.repositories import OrganizationRepositoryImpl
from config.settings import settings


def create_db_session(engine: AsyncEngine):
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    return session_factory()


class Container(containers.DeclarativeContainer):
    db_engine = providers.Singleton(
        create_async_engine,
        settings.db_url.get_secret_value(),
        pool_size=settings.db_pool_size,
        max_overflow=0,
        pool_timeout=30,
    )
    
    db_session = providers.Factory(
        create_db_session,
        engine=db_engine,
    )
    
    organization_repository = providers.Factory(
        OrganizationRepositoryImpl,
        session=db_session,
    )
    organization_service = providers.Factory(OrganizationService, organization_repository=organization_repository)
