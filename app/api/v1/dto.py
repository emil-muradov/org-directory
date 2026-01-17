from pydantic import BaseModel, Field


class GetOrganizationsQueryParams(BaseModel):
    building_id: int = Field()
    industry_id: int = Field()
    name: str = Field()
    lat: float = Field()
    lon: float = Field()
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
