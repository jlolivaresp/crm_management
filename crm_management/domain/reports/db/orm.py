from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey

from crm_management.db.orm_base import Base


class DealAggregationORM(Base):
    __tablename__ = "deal_aggregations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    aggregation_type = Column(String, nullable=False)
    aggregation_date = Column(Date, nullable=False)
    total_deal_size = Column(Float, nullable=False)
    deal_count = Column(Integer, nullable=False)
