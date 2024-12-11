from crm_management.db.service_base import DBBaseAPI
from crm_management.domain.contacts.db.orm import ContactORM


class DBContactsAPI(DBBaseAPI[ContactORM]):
    """Database operations for the Contact domain."""

    def __init__(self, session):
        super().__init__(session, ContactORM)
