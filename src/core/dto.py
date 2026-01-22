from typing import TypedDict
from pydantic import BaseModel, Field


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
    page: int = Field(description="Current page number")
    page_items: int = Field(description="Number of items on the current page")
    has_more: bool = Field(description="Whether there are more pages available")
