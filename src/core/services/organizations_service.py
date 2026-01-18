from persistence.db.repositories import OrganizationsRepository
from ..mappers import map_db_organization_to_dto
from ..dto import OrganizationDTO


class OrganizationsService:
    def __init__(self, organizations_repository: OrganizationsRepository):
        self._organizations_repository = organizations_repository

    def find_organizations(
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
        size: int,
    ) -> tuple[list[OrganizationDTO], bool]:
        if building_id is not None:
            return (
                map(
                    map_db_organization_to_dto,
                    self._organizations_repository.find_organizations_by_building_id(building_id),
                ),
                False,
            )
        if industry_id is not None:
            return (
                map(
                    map_db_organization_to_dto,
                    self._organizations_repository.find_organizations_by_industry_id(industry_id),
                ),
                False,
            )
        if organization_name is not None:
            return (
                map(
                    map_db_organization_to_dto,
                    self._organizations_repository.find_organizations_by_name(organization_name),
                ),
                False,
            )
        if industry_name is not None:
            return (
                map(
                    map_db_organization_to_dto,
                    self._organizations_repository.find_organizations_by_industry_name(industry_name),
                ),
                False,
            )
        if lat is not None and lon is not None:
            return (
                map(
                    map_db_organization_to_dto, self._organizations_repository.find_organizations_by_geo_point(lat, lon)
                ),
                False,
            )
        if polygon_wkt is not None:
            return (
                map(
                    map_db_organization_to_dto,
                    self._organizations_repository.find_organizations_by_geo_area(polygon_wkt),
                ),
                False,
            )

        orgs, has_more = self._organizations_repository.get_all_organizations(size, page * size)
        return (map(map_db_organization_to_dto, orgs), has_more)
