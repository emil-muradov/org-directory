"""Mappers for converting domain entities to presentation DTOs."""

from api.v1.dto import BuildingDTO, OrganizationDTO, PointDTO
from core.entities import Building, Organization


def map_organization_to_dto(organization: Organization) -> OrganizationDTO:
    """Map domain Organization entity to OrganizationDTO."""
    return OrganizationDTO(
        id=organization.id,
        name=organization.name,
        phones=organization.phones,
        building=map_building_to_dto(organization.building),
        industries=organization.industries,
    )


def map_building_to_dto(building: Building) -> BuildingDTO:
    """Map domain Building entity to BuildingDTO."""
    return BuildingDTO(
        id=building.id,
        address=building.address,
        coordinates=PointDTO(lat=building.coordinates["lat"], lon=building.coordinates["lon"]),
    )
