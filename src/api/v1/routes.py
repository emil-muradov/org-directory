from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import Provide, inject

from core.services import OrganizationService
from core.dto import OrganizationDTO, PaginatedResource
from infrastructure.di.container import Container
from .dto import GetOrganizationsQueryParams


router = APIRouter(
    prefix="/v1",
)


@router.get(
    "/organizations/{id}",
    summary="Get organization by ID",
    description="Retrieve a single organization by its unique identifier.",
    response_description="The organization details including name, phones, building information, and industries.",
    responses={
        200: {"description": "Success"},
        404: {"description": "Organization not found"},
    },
    tags=["organizations"],
    operation_id="getOrganizationById",
)
@inject
async def get_organization(
    id: int,
    organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
) -> OrganizationDTO:
    org = await organization_service.find_organization_by_id(id)
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return JSONResponse(content=org.model_dump(), status_code=200)


@router.get(
    "/organizations",
    summary="Search and filter organizations",
    description=(
        "Retrieve a paginated list of organizations with optional filtering capabilities. "
        "Supports filtering by building ID, industry ID or name, organization name, address, "
        "geographic location (point or polygon), and pagination. "
        "Cannot use both point-based (lat/lon) and polygon-based filters together. "
        "A polygon must have at least 3 points."
    ),
    response_description="Paginated list of organizations matching the filter criteria.",
    responses={
        200: {"description": "Success"},
        422: {"description": "Validation error - invalid filter combinations or parameters"},
    },
    tags=["organizations"],
    operation_id="findOrganizations",
)
@inject
async def find_organizations(
    filter_query: Annotated[GetOrganizationsQueryParams, Query()],
    organization_service: OrganizationService = Depends(Provide[Container.organization_service]),
) -> PaginatedResource[OrganizationDTO]:
    orgs = await organization_service.find_organizations(**filter_query.model_dump(exclude_none=True))
    return JSONResponse(content=orgs.model_dump(), status_code=200)
