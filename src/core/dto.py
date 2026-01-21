from pydantic import BaseModel


class BuildingDTO(BaseModel):
    id: int
    address: str
    coordinates: tuple[float, float]


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
