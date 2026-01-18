from typing import Annotated
from fastapi import APIRouter, Query

from dto import GetOrganizationsQueryParams, OrganizationDTO


router = APIRouter(
    prefix="/v1/",
)


@router.get(f"/organizations/{id}")
def get_organization(organization_id: int) -> OrganizationDTO:
    pass


@router.get("/organizations")
def get_organization(filter_query: Annotated[GetOrganizationsQueryParams, Query()]) -> list[OrganizationDTO]:
    pass
