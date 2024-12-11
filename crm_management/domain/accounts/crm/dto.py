from __future__ import annotations

from enum import Enum
from typing import Any

from crm_management.crm.dto_base import BaseDTO


class RegionCRMEnum(Enum):
    NORTH_AMERICA = "North America"
    EUROPE = "Europe"
    ASIA = "Asia"


class AccountDTO(BaseDTO):
    id: int | None
    account_id: int
    account_name: str
    industry: str
    account_value: int
    region: RegionCRMEnum

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AccountDTO:
        custom_fields = data.get("custom_field", {})
        return cls(
            id=data.get("id"),
            account_id=custom_fields.get("cf_account_id"),
            account_name=data.get("name"),
            industry=custom_fields.get("cf_industry"),
            account_value=custom_fields.get("cf_account_value"),
            region=RegionCRMEnum(custom_fields.get("cf_region")),
        )
