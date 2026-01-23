"""Mappers for converting between database and domain layers."""

from geoalchemy2 import WKTElement


def map_point_to_db_point(*, lat: float, lon: float) -> WKTElement | None:
    return WKTElement(f"POINT({lon} {lat})", srid=4326)


def map_polygon_to_db_polygon(polygon: list[tuple[float, float]]) -> WKTElement | None:
    coords = [f"{lon} {lat}" for lat, lon in polygon]
    return WKTElement(f"POLYGON(({', '.join(coords)}))", srid=4326)
