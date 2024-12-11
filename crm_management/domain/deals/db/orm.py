import enum

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum

from crm_management.db.orm_base import Base


class DealStageORMEnum(str, enum.Enum):
    PROSPECTING = "Prospecting"
    NEGOTIATION = "Negotiation"
    CLOSED_WON = "Closed-Won"
    CLOSED_LOST = "Closed-Lost"


class DealORM(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    deal_id = Column(Integer, unique=True, nullable=False)
    deal_name = Column(String, nullable=False)
    deal_size = Column(Integer, nullable=True)
    probability_of_closure = Column(String, nullable=False)
    deal_stage = Column(Enum(DealStageORMEnum), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
