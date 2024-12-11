from crm_management.db.service_base import DBBaseAPI
from crm_management.domain.deals.db.orm import DealORM


class DBDealsAPI(DBBaseAPI[DealORM]):
    """Database operations for the Deal domain."""

    def __init__(self, session):
        super().__init__(session, DealORM)
