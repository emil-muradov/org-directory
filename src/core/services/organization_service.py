from dataclasses import dataclass

from core.mappers import map_point_to_db_point, map_polygon_to_db_polygon
from core.entities import Organization
from infrastructure.persistence.db.repositories import OrganizationRepository
from infrastructure.persistence.mappers import map_db_organization_to_entity


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
        # Validate conflicting filters
        has_point_filter = lat is not None and lon is not None
        has_polygon_filter = polygon is not None

        if has_point_filter and has_polygon_filter:
            raise ValueError(
                "Cannot use both point-based (lat/lon) and polygon-based filters together. "
                "Use either lat/lon or polygon/polygon_wkt."
            )

        # Check if any filters are provided
        has_filters = any(
            [
                building_id is not None,
                industry_id is not None,
                organization_name is not None,
                industry_name is not None,
                address is not None,
                has_point_filter,
                has_polygon_filter,
            ]
        )

        # Calculate pagination
        offset = (page - 1) * items_per_page
        limit = items_per_page + 1  # Fetch one extra to check for more pages

        if has_filters:
            # Use combined filter method
            result = await self._organization_repository.find_organizations_with_filters(
                building_id=building_id,
                industry_id=industry_id,
                organization_name=organization_name,
                industry_name=industry_name,
                address=address,
                point_wkt=map_point_to_db_point(lat=lat, lon=lon),
                polygon_wkt=map_polygon_to_db_polygon(polygon),
                limit=limit,
                offset=offset,
            )
        else:
            # No filters, get all organizations
            result = await self._organization_repository.get_all_organizations(limit=limit, offset=offset)

        return self._build_paginated_response(result, page, items_per_page)

    async def find_organization_by_id(self, organization_id: int) -> Organization | None:
        result = await self._organization_repository.find_organization_by_id(organization_id)
        if result is None:
            return None
        return map_db_organization_to_entity(result)
