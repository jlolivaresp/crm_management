from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from crm_management.db.orm_base import Base


class RegionORMEnum(PyEnum):
    NORTH_AMERICA = "North America"
    EUROPE = "Europe"
    ASIA = "Asia"


class AccountORM(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, unique=True, nullable=False)
    account_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    account_value = Column(Integer, nullable=False)
    region = Column(Enum(RegionORMEnum), nullable=False)
    deals = relationship("DealORM", backref="accounts")
