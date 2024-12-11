from typing import Any

from crm_management.domain.contacts.crm.service import CRMContactsAPI
from crm_management.domain.contacts.db.service import DBContactsAPI
from crm_management.domain.contacts.crm.dto import ContactDTO, LeadSourceCRMEnum
from crm_management.domain.contacts.db.orm import ContactORM, LeadSourceORMEnum
from crm_management.services.base import ServiceBase


class ServiceContact(ServiceBase[ContactDTO, ContactORM]):
    def __init__(self, crm_api: CRMContactsAPI, domain_api: DBContactsAPI):
        super().__init__(crm_api=crm_api, domain_api=domain_api)
        self.crm_api = crm_api
        self.domain_api = domain_api

    def find_all(self) -> list[ContactDTO]:
        return super().find_all()

    def find_by_id(self, entity_id: str) -> ContactDTO | None:
        return super().find_by_id(entity_id=entity_id)

    def find_by_field_name(self, field_name: str, value: Any) -> list[ContactDTO]:
        return super().find_by_field_name(field_name=field_name, value=value)

    def update_one(self, updated_data: ContactDTO) -> ContactDTO:
        return super().update_one(updated_data=updated_data)

    def clean_crm_data(self, data: list[ContactDTO]) -> list[ContactDTO]:
        deduplicated_data = self._remove_duplicates(data=data, keys=["contact_id"])
        return self._handle_missing_values(deduplicated_data)

    def _crm_dto_from_orm(self, data: ContactORM) -> ContactDTO:
        return ContactDTO(
            id=data.id,
            contact_id=data.contact_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            job_title=data.job_title,
            lead_source=LeadSourceCRMEnum(data.lead_source),
            last_contact_date=data.last_contact_date,
        )

    def _orm_from_crm_dto(self, data: ContactDTO) -> ContactORM:
        return ContactORM(
            id=data.id,
            contact_id=data.contact_id,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            job_title=data.job_title,
            lead_source=LeadSourceORMEnum(data.lead_source),
            last_contact_date=data.last_contact_date,
        )

    def has_changes(self, crm_data: ContactDTO, db_data: ContactORM) -> bool:
        return (
            crm_data.contact_id != db_data.contact_id
            or crm_data.first_name != db_data.first_name
            or crm_data.last_name != db_data.last_name
            or crm_data.email != db_data.email
            or crm_data.job_title != db_data.job_title
            or crm_data.lead_source != db_data.lead_source
            or crm_data.last_contact_date != db_data.last_contact_date
        )
