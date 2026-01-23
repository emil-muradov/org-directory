from pydantic import BaseModel, model_validator, Field


class GetOrganizationsQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    building_id: int | None = Field(None, description="Filter by building ID (exact match)")
    industry_id: int | None = Field(None, description="Filter by industry ID (exact match)")
    industry_name: str | None = Field(None, description="Filter by industry name (partial match)")
    organization_name: str | None = Field(None, description="Filter by organization name (partial match)")
    address: str | None = Field(None, description="Filter by address (partial match)")
    polygon: list[(float, float)] | None = Field(
        None,
        description="Filter by geographic polygon - list of (latitude, longitude) tuples. Minimum 3 points required.",
    )
    lat: float | None = Field(None, description="Latitude for point-based filtering. Must be provided together with lon.")
    lon: float | None = Field(None, description="Longitude for point-based filtering. Must be provided together with lat.")
    page: int = Field(gt=0, default=1, description="Page number (must be greater than 0)")
    items_per_page: int = Field(gt=0, default=50, description="Number of items per page (must be greater than 0)")

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
