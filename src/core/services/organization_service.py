from infrastructure.persistence.db.repositories import OrganizationRepository
from core.data_mappers import map_db_organization_to_dto
from core.dto import OrganizationDTO, PaginatedResource


class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository):
        self._organization_repository = organization_repository

    async def find_organizations(
        self,
        *,
        building_id: int | None = None,
        industry_id: int | None = None,
        organization_name: str | None = None,
        industry_name: str | None = None,
        polygon_wkt: str | None = None,
        lat: float | None = None,
        lon: float | None = None,
        page: int,
        items_per_page: int,
    ) -> PaginatedResource[OrganizationDTO]:
        if building_id is not None:
            result = await self._organization_repository.find_organizations_by_building_id(building_id)
            return PaginatedResource(
                items=list(map(map_db_organization_to_dto, result)),
                has_more=False,
                page=page,
                items_per_page=items_per_page,
            )
        if industry_id is not None:
            result = await self._organization_repository.find_organizations_by_industry_id(industry_id)
            return PaginatedResource(
                items=list(map(map_db_organization_to_dto, result)),
                has_more=False,
                page=page,
                items_per_page=items_per_page,
            )
        if organization_name is not None:
            result = await self._organization_repository.find_organizations_by_name(organization_name)
            return PaginatedResource(
                items=list(map(map_db_organization_to_dto, result)),
                has_more=False,
                page=page,
                items_per_page=items_per_page,
            )
        if industry_name is not None:
            result = await self._organization_repository.find_organizations_by_industry_name(industry_name)
            return PaginatedResource(
                items=list(map(map_db_organization_to_dto, result)),
                has_more=False,
                page=page,
                items_per_page=items_per_page,
            )
        if lat is not None and lon is not None:
            result = await self._organization_repository.find_organizations_by_geo_point(lat, lon)
            return PaginatedResource(
                items=list(map(map_db_organization_to_dto, result)),
                has_more=False,
                page=page,
                items_per_page=items_per_page,
            )
        if polygon_wkt is not None:
            result = await self._organization_repository.find_organizations_by_geo_area(polygon_wkt)
            return PaginatedResource(
                items=list(map(map_db_organization_to_dto, result)),
                has_more=False,
                page=page,
                items_per_page=items_per_page,
            )

        result = await self._organization_repository.get_all_organizations(
            limit=items_per_page + 1, offset=page * items_per_page
        )
        return PaginatedResource(
            items=map(map_db_organization_to_dto, result[:items_per_page]),
            has_more=len(result) > items_per_page,
            page=page,
            items_per_page=items_per_page,
        )

    async def find_organization_by_id(self, organization_id: int) -> OrganizationDTO | None:
        result = await self._organization_repository.find_organization_by_id(organization_id)
        if result is None:
            return None
        return map_db_organization_to_dto(result)
