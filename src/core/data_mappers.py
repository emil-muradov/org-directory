from infrastructure.persistence.db.schema import Organization, Building, Industry
from core.dto import BuildingDTO, OrganizationDTO


def map_db_organization_to_dto(db_organization: Organization) -> OrganizationDTO:
    return OrganizationDTO(
        id=db_organization.id,
        name=db_organization.name,
        phones=[phone.phone_number for phone in db_organization.phones],
        building=map_db_building_to_dto(db_organization.building),
        industries=[industry.name for industry in db_organization.industries],
    )


def map_db_building_to_dto(db_building: Building) -> BuildingDTO:
    return BuildingDTO(id=db_building.id, address=db_building.address, coordinates=list(db_building.coordinates))


def map_db_industry_to_dto(db_industry: Industry) -> list[str]:
    pass
