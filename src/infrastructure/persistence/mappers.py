"""Mappers for converting database schemas to domain entities."""

from geoalchemy2.shape import to_shape

from core.entities import Building, Organization, Point
from infrastructure.persistence.db.schema import Building as DBBuilding, Organization as DBOrganization


def map_db_organization_to_entity(db_organization: DBOrganization) -> Organization:
    """Map database Organization schema to domain Organization entity."""
    building = map_db_building_to_entity(db_organization.building)

    return Organization(
        id=db_organization.id,
        name=db_organization.name,
        phones=[phone.phone_number for phone in db_organization.phones],
        building=building,
        industries=[industry.name for industry in db_organization.industries],
    )


def map_db_building_to_entity(db_building: DBBuilding) -> Building:
    """Map database Building schema to domain Building entity."""
    point = to_shape(db_building.coordinates)
    return Building(
        id=db_building.id,
        address=db_building.address,
        coordinates=Point(lat=point.y, lon=point.x),
    )
