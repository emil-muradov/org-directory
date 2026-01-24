from typing import TypedDict

from pydantic import BaseModel, Field, field_validator, model_validator

from core.entities import Point


class PointDTO(TypedDict):
    lat: float
    lon: float


class BuildingDTO(BaseModel):
    id: int = Field(description="Building unique identifier")
    address: str = Field(description="Building address")
    coordinates: PointDTO = Field(description="Geographic coordinates of the building")


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


class GetOrganizationsQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    building_id: int | None = Field(None, description="Filter by building ID (exact match)")
    industry_id: int | None = Field(None, description="Filter by industry ID (exact match)")
    industry_name: str | None = Field(None, description="Filter by industry name (partial match)")
    organization_name: str | None = Field(None, description="Filter by organization name (partial match)")
    address: str | None = Field(None, description="Filter by address (partial match)")
    polygon: list[tuple[float, float]] | None = Field(
        None,
        description="Filter by geographic polygon - list of comma-separated 'lat,lon' coordinates. Minimum 3 points required. Example: ?polygon=40.730,-73.936&polygon=40.730,-73.934",
    )
    lat: float | None = Field(
        None, description="Latitude for point-based filtering. Must be provided together with lon."
    )
    lon: float | None = Field(
        None, description="Longitude for point-based filtering. Must be provided together with lat."
    )
    page: int = Field(gt=0, default=1, description="Page number (must be greater than 0)")
    items_per_page: int = Field(gt=0, default=50, description="Number of items per page (must be greater than 0)")

    @field_validator("polygon", mode="before")
    @classmethod
    def validate_polygon(cls, v: any):
        if isinstance(v, list):
            parsed = []
            for coord_str in v:
                if isinstance(coord_str, str):
                    parts = coord_str.split(",")
                    if len(parts) != 2:
                        raise ValueError(f"Invalid coordinate format: {coord_str}. Expected 'lat,lon'")
                    try:
                        lat = float(parts[0].strip())
                        lon = float(parts[1].strip())
                        parsed.append((lat, lon))
                    except ValueError as e:
                        raise ValueError(f"Invalid coordinate values: {coord_str}. {e}")
                elif isinstance(coord_str, tuple):
                    parsed.append(coord_str)
                else:
                    raise ValueError(f"Invalid coordinate type: {type(coord_str)}")
            return parsed
        return v

    @model_validator(mode="after")
    def validate_params(self):
        """Validate filter combinations."""
        # Check that lat and lon are provided together
        if (self.lat is None) != (self.lon is None):
            raise ValueError("Both lat and lon must be provided together, or neither.")

        if self.lat and self.lon and self.polygon:
            raise ValueError(
                "Cannot use both point-based (lat/lon) and polygon-based filters together. "
                "Use either lat/lon or polygon."
            )

        if self.polygon and len(self.polygon) < 3:
            raise ValueError("A polygon should have at least 3 points.")

        return self
