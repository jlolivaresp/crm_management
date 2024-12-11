from enum import Enum as PyEnum

from sqlalchemy import Column, String, Integer, Enum

from crm_management.db.orm_base import Base


class LeadSourceORMEnum(PyEnum):
    WEBSITE = "Website"
    REFERRAL = "Referral"
    EMAIL_CAMPAIGN = "Email Campaign"


class ContactORM(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    job_title = Column(String, nullable=True)
    lead_source = Column(Enum(LeadSourceORMEnum), nullable=False)
    last_contact_date = Column(String, nullable=True)
