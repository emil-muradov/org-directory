from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from schema import Organization, Industry


class OrganizationsRepository(ABC):
    @abstractmethod
    def find_organization_by_id(self, organization_id: int) -> Organization:
        pass

    @abstractmethod
    def find_organizations_by_name(self, name: str) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_in_building(self, building_id: int) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_in_industry(self, industry_id: int) -> list[Organization]:
        pass

class OrganizationsRepositoryImpl(OrganizationsRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_organization_by_id(self, organization_id: int) -> Organization:
        return self.session.query(Organization).filter(Organization.id == organization_id).first()

    def find_organizations_in_industry(self, industry_id: int) -> list[Organization]:
        return self.session.query(Organization).join(Organization.industries).filter(Industry.id == industry_id).all()