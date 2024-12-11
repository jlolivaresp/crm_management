from crm_management.db.service_base import DBBaseAPI
from crm_management.domain.accounts.db.orm import AccountORM


class DBAccountsAPI(DBBaseAPI[AccountORM]):
    """Database operations for the Account domain."""

    def __init__(self, session):
        super().__init__(session, AccountORM)
