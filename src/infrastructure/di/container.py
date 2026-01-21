from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.services import OrganizationService
from infrastructure.persistence.db.repositories import OrganizationRepositoryImpl
from config.settings import settings



class Container(containers.DeclarativeContainer):
    db_engine = create_async_engine(
        settings.db_url.get_secret_value(),
        pool_size=settings.db_pool_size,
        max_overflow=0,
        pool_timeout=30,
    )
    async_session_factory = async_sessionmaker(db_engine, expire_on_commit=False)
    db_session = providers.Factory(async_session_factory)
    organization_repository = providers.Factory(
        OrganizationRepositoryImpl,
        session=db_session,
    )
    organization_service = providers.Factory(OrganizationService, organization_repository=organization_repository)
