from __future__ import annotations

from enum import Enum
from typing import Any

from crm_management.crm.dto_base import BaseDTO


class LeadSourceCRMEnum(Enum):
    WEBSITE = "Website"
    REFERRAL = "Referral"
    EMAIL_CAMPAIGN = "Email Campaign"


class ContactDTO(BaseDTO):
    id: int | None
    contact_id: str
    first_name: str
    last_name: str
    email: str
    job_title: str | None
    lead_source: LeadSourceCRMEnum
    last_contact_date: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContactDTO:
        custom_fields = data.get("custom_field", {})
        return cls(
            id=data.get("id"),
            contact_id=data.get("external_id", ""),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            email=data.get("email", ""),
            job_title=custom_fields.get("job_title"),
            lead_source=LeadSourceCRMEnum(custom_fields.get("cf_lead_source")),
            last_contact_date=custom_fields.get("cf_last_contacted_date"),
        )
