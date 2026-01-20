from pydantic import BaseModel, model_validator


class GetOrganizationsQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    building_id: int | None = None
    industry_id: int | None = None
    organization_name: str | None = None
    address: str | None = None
    polygon: list[tuple(float, float)] | None = None
    lat: float | None = (None,)
    lon: float | None = (None,)
    page: int = 1
    items_per_page: int = 100

    @model_validator(mode="after")
    def check_geometry_point(self):
        if (self.lat is None) != (self.lon is None):
            raise ValueError("Both lat and lon must be provided together, or neither.")
        return self
