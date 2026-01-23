from geoalchemy2 import WKTElement
from geoalchemy2.shape import to_shape

from infrastructure.persistence.db.schema import Organization as DbOrganization, Building as DbBuilding
from .entities import Point, Organization, Building


def map_point_to_db_point(*, lat: float, lon: float) -> WKTElement | None:
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


def map_polygon_to_db_polygon(polygon: list[tuple[float, float]]) -> WKTElement | None:
    coords = [f"{lon} {lat}" for lat, lon in polygon]
    return WKTElement(f"POLYGON(({', '.join(coords)}))", srid=4326)


def map_db_organization_to_entity(db_organization: DbOrganization) -> Organization:
    building = map_db_building_to_entity(db_organization.building)

    return Organization(
        id=db_organization.id,
        name=db_organization.name,
        phones=[phone.phone_number for phone in db_organization.phones],
        building=building,
        industries=[industry.name for industry in db_organization.industries],
    )


def map_db_building_to_entity(db_building: DbBuilding) -> Building:
    point = to_shape(db_building.coordinates)
    return Building(
        id=db_building.id,
        address=db_building.address,
        coordinates=Point(lat=point.y, lon=point.x),
    )
