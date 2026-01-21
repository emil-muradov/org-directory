from typing import Annotated

from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from core.services import OrganizationService
from core.dto import OrganizationDTO
from infrastructure.di.container import Container
from .dto import GetOrganizationsQueryParams


router = APIRouter(
    prefix="/v1",
)


@router.get(f"/organizations/{id}")
@inject
async def get_organization(
    organization_id: int,
    organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
) -> OrganizationDTO:
    org = await organization_service.find_organization_by_id(organization_id)
    if org is None:
        return JSONResponse(status_code=404)
    return JSONResponse(content=org.model_dump(), status_code=200)


@router.get("/organizations")
@inject
async def find_organizations(
    filter_query: Annotated[GetOrganizationsQueryParams, Query()],
    organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
) -> list[OrganizationDTO]:
    orgs = await organization_service.find_organizations(**filter_query.model_dump(exclude_none=True))
    return JSONResponse(content=orgs.model_dump(), status_code=200)
