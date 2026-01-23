from typing import TypedDict
from pydantic import BaseModel, Field


class Point(TypedDict):
    lat: float
    lon: float


class BuildingDTO(BaseModel):
    id: int = Field(description="Building unique identifier")
    address: str = Field(description="Building address")
    coordinates: Point = Field(description="Geographic coordinates of the building")


class OrganizationDTO(BaseModel):
    id: int = Field(description="Organization unique identifier")
    name: str = Field(description="Organization name")
    phones: list[str] = Field(description="List of phone numbers")
    building: BuildingDTO = Field(description="Building information")
    industries: list[str] = Field(description="List of industry names")


class PaginatedResource[T](BaseModel):
    items: list[T] = Field(description="List of items on the current page")
    page: int = Field(description="Current page number")
    page_items: int = Field(description="Number of items on the current page")
    has_more: bool = Field(description="Whether there are more pages available")
