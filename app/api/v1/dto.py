from pydantic import BaseModel, model_validator


class GetOrganizationsQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    building_id: int | None = None
    industry_id: int | None = None
    name: str | None = None
    address: str | None = None
    lat: float | None = None
    lon: float | None = None
    limit: int = 100
    offset: int = 0

    @model_validator(mode="after")
    def check_geometry_point(self):
        if (self.lat is None) != (self.lon is None):
            raise ValueError("Both lat and lon must be provided together, or neither.")
        return self


class BuildingDTO(BaseModel):
    building_id: int
    address: str
    coordinates: tuple[float, float]


class OrganizationDTO(BaseModel):
    name: str
    phones: list[str]
    building: BuildingDTO
    industries: list[str]
