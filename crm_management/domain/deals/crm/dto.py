from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from crm_management.crm.dto_base import BaseDTO


class DealStageCRMEnum(Enum):
    PROSPECTING = "Prospecting"
    NEGOTIATION = "Negotiation"
    CLOSED_WON = "Closed-Won"
    CLOSED_LOST = "Closed-Lost"


class DealDTO(BaseDTO):
    id: int
    deal_id: int
    deal_name: str | None
    deal_size: int | None
    probability_of_closure: str | None
    deal_stage: DealStageCRMEnum
    account_id: int
    created_at: datetime

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DealDTO:
        custom_fields = data.get("custom_field", {})
        return cls(
            id=data.get("id"),
            deal_id=custom_fields.get("cf_deal_id"),
            deal_name=data.get("name"),
            deal_size=float(data.get("amount")),
            probability_of_closure=custom_fields.get("cf_probability_of_closure", ""),
            deal_stage=DealStageCRMEnum(custom_fields.get("cf_deal_stage")),
            account_id=custom_fields.get("cf_account_id"),
            created_at=data.get("created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "amount": self.deal_size,
            "created_at": self.created_at.isoformat(),
            "custom_field": {
                "cf_account_id": self.account_id,
                "cf_deal_stage": self.deal_stage,
                "cf_probability_of_closure": self.probability_of_closure,
                "cf_deal_id": self.deal_id,
            },
        }
