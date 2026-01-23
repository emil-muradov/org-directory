"""Domain entities - pure business objects without presentation concerns."""

from dataclasses import dataclass
from typing import TypedDict


class Point(TypedDict):
    lat: float
    lon: float


@dataclass
class Building:
    id: int
    address: str
    coordinates: Point


@dataclass
class Organization:
    id: int
    name: str
    phones: list[str]
    building: Building
    industries: list[str]
