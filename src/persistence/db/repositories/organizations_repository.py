from abc import ABC, abstractmethod

from sqlalchemy import or_, func
from sqlalchemy.orm import Session, aliased
from geoalchemy2.elements import WKTElement

from schema import Organization, Industry, Building


class OrganizationsRepository(ABC):
    @abstractmethod
    def find_organization_by_id(self, organization_id: int) -> Organization:
        pass

    @abstractmethod
    def find_organizations_by_name(self, name: str) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_by_building_id(self, building_id: int) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_by_industry_id(self, industry_id: int) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_by_geo_point(self, lat: float, lon: float) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_by_geo_area(self, polygon_wkt: str) -> list[Organization]:
        pass

    @abstractmethod
    def find_organizations_by_industry_name(self, industry_name: str) -> list[Organization]:
        pass


class OrganizationsRepositoryImpl(OrganizationsRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_organization_by_id(self, organization_id: int) -> Organization:
        return self.session.query(Organization).filter(Organization.id == organization_id).first()

    def find_organizations_by_building_id(self, building_id: int) -> list[Organization]:
        return self.session.query(Organization).filter(Organization.building_id == building_id).all()

    def find_organizations_by_industry_id(self, industry_id: int) -> list[Organization]:
        return self.session.query(Organization).join(Organization.industries).filter(Industry.id == industry_id).all()

    def find_organizations_by_geo_point(self, lat: float, lon: float) -> list[Organization]:
        point = WKTElement(f"POINT({lon} {lat})", srid=4326)
        # Find organizations within 100 meters of the point (0.001 degrees ≈ 100m at equator)
        return (
            self.session.query(Organization)
            .join(Organization.building)
            .filter(func.ST_DWithin(Building.coordinates, point, 0.001))
            .all()
        )

    def find_organizations_by_geo_area(self, polygon_wkt: str) -> list[Organization]:
        polygon = WKTElement(polygon_wkt, srid=4326)
        return (
            self.session.query(Organization)
            .join(Organization.building)
            .filter(func.ST_Contains(polygon, Building.coordinates))
            .all()
        )

    def find_organizations_by_industry_name(self, industry_name: str) -> list[Organization]:
        parent1 = aliased(Industry)
        parent2 = aliased(Industry)
        parent3 = aliased(Industry)

        return (
            self.session.query(Organization)
            .join(Organization.industries)
            .outerjoin(parent1, Industry.parent_id == parent1.id)
            .outerjoin(parent2, parent1.parent_id == parent2.id)
            .outerjoin(parent3, parent2.parent_id == parent3.id)
            .filter(
                or_(
                    Industry.name.ilike(f"%{industry_name}%"),
                    parent1.name.ilike(f"%{industry_name}%"),
                    parent2.name.ilike(f"%{industry_name}%"),
                    parent3.name.ilike(f"%{industry_name}%"),
                )
            )
            .distinct()
            .all()
        )
