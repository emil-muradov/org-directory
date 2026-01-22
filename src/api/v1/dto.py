from pydantic import BaseModel, model_validator, Field


class GetOrganizationsQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    building_id: int | None = None
    industry_id: int | None = None
    industry_name: str | None = None
    organization_name: str | None = None
    address: str | None = None
    polygon: list[(float, float)] | None = None
    lat: float | None = None
    lon: float | None = None
    page: int = Field(gt=0, default=1)
    items_per_page: int = Field(gt=0, default=50)

    @model_validator(mode="after")
    def validate_filters(self):
        """Validate filter combinations."""
        # Check that lat and lon are provided together
        if (self.lat is None) != (self.lon is None):
            raise ValueError("Both lat and lon must be provided together, or neither.")

        # Check for conflicting geometry filters
        has_point_filter = self.lat is not None and self.lon is not None
        has_polygon_filter = self.polygon is not None

        if has_point_filter and has_polygon_filter:
            raise ValueError(
                "Cannot use both point-based (lat/lon) and polygon-based filters together. "
                "Use either lat/lon or polygon."
            )

        if self.polygon and len(self.polygon) < 3:
            raise ValueError("A polygon should have at least 3 points.")

        return self
