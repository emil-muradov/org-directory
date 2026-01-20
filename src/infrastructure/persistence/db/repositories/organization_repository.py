from abc import ABC, abstractmethod

from sqlalchemy import or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from geoalchemy2.elements import WKTElement

from schema import Organization, Industry, Building


class OrganizationRepository(ABC):
    @abstractmethod
    async def get_all_organizations(self, *, limit: int, offset: int) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organization_by_id(self, organization_id: int) -> Organization | None:
        pass

    @abstractmethod
    async def find_organizations_by_name(self, name: str) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_building_id(self, building_id: int) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_industry_id(self, industry_id: int) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_geo_point(self, lat: float, lon: float) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_geo_area(self, polygon_wkt: str) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_industry_name(self, industry_name: str) -> list[Organization]:
        pass


class OrganizationRepositoryImpl(OrganizationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_organizations(self, *, limit: int, offset: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .order_by(Organization.created_at)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organization_by_id(self, organization_id: int) -> Organization | None:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .filter(Organization.id == organization_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_organizations_by_name(self, name: str) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .filter(Organization.name.ilike(f"%{name}%"))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_building_id(self, building_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .filter(Organization.building_id == building_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_industry_id(self, industry_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .filter(Industry.id == industry_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_geo_point(self, lat: float, lon: float) -> list[Organization]:
        point = WKTElement(f"POINT({lon} {lat})", srid=4326)
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .filter(func.ST_DWithin(Building.coordinates, point, 0.001))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_geo_area(self, polygon_wkt: str) -> list[Organization]:
        polygon = WKTElement(polygon_wkt, srid=4326)
        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
            .join(Organization.industries)
            .filter(func.ST_Contains(polygon, Building.coordinates))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_industry_name(self, industry_name: str) -> list[Organization]:
        parent1 = aliased(Industry)
        parent2 = aliased(Industry)
        parent3 = aliased(Industry)

        stmt = (
            select(Organization)
            .join(Organization.building)
            .join(Organization.phones)
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
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
