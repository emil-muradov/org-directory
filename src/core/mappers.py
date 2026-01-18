from persistence.db.schema import Organization, Building, Industry, Phone
from .dto import OrganizationDTO


def map_db_organization_to_dto(db_organization: Organization) -> OrganizationDTO:
    return OrganizationDTO(
        id=db_organization.id,
        name=db_organization.name,
        phones=db_organization.phones,
        building=db_organization.building,
        industries=db_organization.industries,
    )
