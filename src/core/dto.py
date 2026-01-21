from typing import TypedDict
from pydantic import BaseModel


class Point(TypedDict):
    lat: float
    lon: float


class BuildingDTO(BaseModel):
    id: int
    address: str
    coordinates: Point


class OrganizationDTO(BaseModel):
    id: int
    name: str
    phones: list[str]
    building: BuildingDTO
    industries: list[str]


class PaginatedResource[T](BaseModel):
    items: list[T]
    page: int
    has_more: bool
    items_per_page: int
