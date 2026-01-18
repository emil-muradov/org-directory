from typing import Annotated
from fastapi import APIRouter, Query, Depends
from dependency_injector.wiring import Provide, inject

from .dto import GetOrganizationsQueryParams, OrganizationDTO
from core.services import OrganizationsService
from persistence.di.container import Container


router = APIRouter(
    prefix="/v1/",
)


@router.get(f"/organizations/{id}")
@inject
def get_organization(
    organization_id: int,
    organizations_service: OrganizationsService = Depends(Provide[Container.organizations_service]),
) -> OrganizationDTO:
    pass


@router.get("/organizations")
@inject
def get_organization(
    filter_query: Annotated[GetOrganizationsQueryParams, Query()],
    organizations_service: OrganizationsService = Depends(Provide[Container.organizations_service]),
) -> list[OrganizationDTO]:
    pass
