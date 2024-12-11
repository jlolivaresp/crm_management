from crm_management.db.service_base import DBBaseAPI
from crm_management.domain.reports.db.orm import DealAggregationORM


class DBDealsAggregationAPI(DBBaseAPI[DealAggregationORM]):
    """Database operations for the Deal Aggregation domain."""

    def __init__(self, session):
        super().__init__(session, DealAggregationORM)
