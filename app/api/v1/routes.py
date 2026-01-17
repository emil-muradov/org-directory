from typing import Annotated
from fastapi import APIRouter, Query

from dto import GetOrganizationsQueryParams


router = APIRouter(
    prefix="/v1/",
)


@router.get(f"/organizations/{id}")
def get_organization(organization_id: int) -> any:
    pass


@router.get("/organizations")
def get_organization(filter_query: Annotated[GetOrganizationsQueryParams, Query()]) -> list[any]:
    pass
