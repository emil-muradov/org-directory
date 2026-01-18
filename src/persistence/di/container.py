from dependency_injector import containers, providers
from sqlalchemy.orm import sessionmaker

from core.services import OrganizationsService
from persistence.db.repositories import OrganizationsRepositoryImpl
from persistence.db.engine import create_db_engine
from config.settings import settings


class Container(containers.DeclarativeContainer):
    db_engine = create_db_engine(settings.db_url)
    db_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
    )

    organizations_repository = providers.Factory(
        OrganizationsRepositoryImpl,
        session=db_session,
    )

    organizations_service = providers.Factory(OrganizationsService, organizations_repository=organizations_repository)
