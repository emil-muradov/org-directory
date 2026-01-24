from abc import ABC, abstractmethod

from sqlalchemy import or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload
from geoalchemy2.elements import WKTElement

from infrastructure.persistence.db.schema import Organization, Industry, Building


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
    async def find_organizations_by_geo_point(self, point_wkt: WKTElement) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_geo_area(self, polygon_wkt: WKTElement) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_by_industry_name(self, industry_name: str) -> list[Organization]:
        pass

    @abstractmethod
    async def find_organizations_with_filters(
        self,
        *,
        building_id: int | None = None,
        industry_id: int | None = None,
        organization_name: str | None = None,
        industry_name: str | None = None,
        address: str | None = None,
        point_wkt: WKTElement | None = None,
        polygon_wkt: WKTElement | None = None,
        limit: int,
        offset: int,
    ) -> list[Organization]:
        pass


class OrganizationRepositoryImpl(OrganizationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_organizations(self, *, limit: int, offset: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organization_by_id(self, organization_id: int) -> Organization | None:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .filter(Organization.id == organization_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_organizations_by_name(self, name: str) -> list[Organization]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .filter(Organization.name.ilike(f"%{name}%"))
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_building_id(self, building_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .filter(Organization.building_id == building_id)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_industry_id(self, industry_id: int) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.industries)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .filter(Industry.id == industry_id)
            .distinct()
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_geo_point(self, point_wkt: WKTElement) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .filter(func.ST_DWithin(Building.coordinates, point, 0.001))
            .distinct()
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_geo_area(self, polygon_wkt: WKTElement) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .filter(func.ST_Contains(polygon_wkt, Building.coordinates))
            .distinct()
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def find_organizations_by_industry_name(self, industry_name: str) -> list[Organization]:
        parent1 = aliased(Industry)
        parent2 = aliased(Industry)
        parent3 = aliased(Industry)

        stmt = (
            select(Organization)
            .join(Organization.industries)
            .outerjoin(parent1, Industry.parent_id == parent1.id)
            .outerjoin(parent2, parent1.parent_id == parent2.id)
            .outerjoin(parent3, parent2.parent_id == parent3.id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
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

    async def find_organizations_with_filters(
        self,
        *,
        building_id: int | None = None,
        industry_id: int | None = None,
        organization_name: str | None = None,
        industry_name: str | None = None,
        address: str | None = None,
        point_wkt: WKTElement | None = None,
        polygon_wkt: WKTElement | None = None,
        limit: int,
        offset: int,
    ) -> list[Organization]:
        """
        Find organizations by many parameters combined.
        All provided filters are combined with AND.
        """
        stmt = select(Organization)

        if any([address, point_wkt, polygon_wkt]):
            stmt = stmt.join(Organization.building)

        if any([industry_id, industry_name]):
            stmt = stmt.join(Organization.industries)

        if industry_name:
            parent1 = aliased(Industry)
            parent2 = aliased(Industry)
            parent3 = aliased(Industry)

            stmt = (
                stmt.outerjoin(parent1, Industry.parent_id == parent1.id)
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
            )

        if industry_id:
            stmt = stmt.filter(Industry.id == industry_id)

        if building_id:
            stmt = stmt.filter(Organization.building_id == building_id)

        if organization_name:
            stmt = stmt.filter(Organization.name.ilike(f"%{organization_name}%"))

        if address:
            stmt = stmt.filter(Building.address.ilike(f"%{address}%"))

        if point_wkt:
            stmt = stmt.filter(func.ST_DWithin(Building.coordinates, point_wkt, 0.001))

        if polygon_wkt:
            stmt = stmt.filter(func.ST_Contains(polygon_wkt, Building.coordinates))

        stmt = (
            stmt.options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.industries),
            )
            .distinct()
            .limit(limit)
            .offset(offset)
        )

        result = await self._session.execute(stmt)
        return list(result.scalars().all())
