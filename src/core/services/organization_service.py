from dataclasses import dataclass

from core.mappers import map_point_to_db_point, map_polygon_to_db_polygon, map_db_organization_to_entity
from core.entities import Organization
from infrastructure.persistence.db.repositories import OrganizationRepository


@dataclass
class PaginatedResult[T]:
    items: list[T]
    page: int
    page_items: int
    has_more: bool


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository):
        self._organization_repository = organization_repository

    def _build_paginated_response(self, results: list, page: int, items_per_page: int) -> PaginatedResult[Organization]:
        domain_entities = [map_db_organization_to_entity(org) for org in results[:items_per_page]]
        has_more = len(results) > items_per_page

        return PaginatedResult(
            items=domain_entities,
            has_more=has_more,
            page=page,
            page_items=len(results),
        )

    async def find_organizations(
        self,
        *,
        building_id: int | None = None,
        industry_id: int | None = None,
        organization_name: str | None = None,
        industry_name: str | None = None,
        address: str | None = None,
        polygon: list[tuple[float, float]] | None = None,
        lat: float | None = None,
        lon: float | None = None,
        page: int,
        items_per_page: int,
    ) -> PaginatedResult[Organization]:
        offset = (page - 1) * items_per_page
        limit = items_per_page + 1  # Fetch one extra to check for more pages

        if any(
            [
                building_id,
                industry_id,
                organization_name,
                industry_name,
                address,
                lat and lon,
                polygon,
            ]
        ):
            result = await self._organization_repository.find_organizations_with_filters(
                building_id=building_id,
                industry_id=industry_id,
                organization_name=organization_name,
                industry_name=industry_name,
                address=address,
                point_wkt=map_point_to_db_point(lat=lat, lon=lon) if lat and lon else None,
                polygon_wkt=map_polygon_to_db_polygon(polygon) if polygon else None,
                limit=limit,
                offset=offset,
            )
        else:
            result = await self._organization_repository.get_all_organizations(limit=limit, offset=offset)

        return self._build_paginated_response(result, page, items_per_page)

    async def find_organization_by_id(self, organization_id: int) -> Organization | None:
        result = await self._organization_repository.find_organization_by_id(organization_id)
        if result is None:
            return None
        return map_db_organization_to_entity(result)
