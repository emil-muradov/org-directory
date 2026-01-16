from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Index
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from geoalchemy2 import Geometry


class Base(AsyncAttrs, DeclarativeBase):
    pass


organization_industries = Table(
    "organization_industries",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("industry_id", Integer, ForeignKey("industries.id"), primary_key=True),
    Column("created_at", DateTime, default=func.now()),
)


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(), nullable=False, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    phones = relationship("Phone", back_populates="organization")
    building = relationship("Building", back_populates="organizations")
    industries = relationship("Industry", secondary=organization_industries, back_populates="organizations")


Index("idx_organizations_name", Organization.name, postgresql_using="gin")


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)
    phone_number = Column(String(), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    organization = relationship("Organization", back_populates="phones")


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    coordinates = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    organizations = relationship("Organization", back_populates="building")


class Industry(Base):
    __tablename__ = "industries"
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("industries.id"))
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    organizations = relationship("Organization", secondary=organization_industries, back_populates="industries")
    parent = relationship("Industry")
