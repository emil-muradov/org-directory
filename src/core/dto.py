from pydantic import BaseModel


class BuildingDTO(BaseModel):
    building_id: int
    address: str
    coordinates: tuple[float, float]


class OrganizationDTO(BaseModel):
    name: str
    phones: list[str]
    building: BuildingDTO
    industries: list[str]
