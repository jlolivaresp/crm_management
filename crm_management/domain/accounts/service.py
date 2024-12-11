from typing import Any

from crm_management.domain.accounts.crm.dto import AccountDTO, RegionCRMEnum
from crm_management.domain.accounts.crm.service import CRMAccountsAPI
from crm_management.domain.accounts.db.service import DBAccountsAPI
from crm_management.domain.accounts.db.orm import AccountORM, RegionORMEnum
from crm_management.services.base import ServiceBase


class ServiceAccount(ServiceBase[AccountDTO, AccountORM]):
    def __init__(self, crm_api: CRMAccountsAPI, domain_api: DBAccountsAPI):
        super().__init__(crm_api=crm_api, domain_api=domain_api)
        self.crm_api = crm_api
        self.domain_api = domain_api

    def find_all(self) -> list[AccountDTO]:
        return super().find_all()

    def find_by_id(self, entity_id: str) -> AccountDTO | None:
        return super().find_by_id(entity_id=entity_id)

    def find_by_field_name(self, field_name: str, value: Any) -> list[AccountDTO]:
        return super().find_by_field_name(field_name=field_name, value=value)

    def update_one(self, updated_data: AccountDTO) -> AccountDTO:
        return super().update_one(updated_data=updated_data)

    def clean_crm_data(self, data: list[AccountDTO]) -> list[AccountDTO]:
        deduplicated_data = self._remove_duplicates(
            data=data, keys=["account_id", "account_name"]
        )
        return self._handle_missing_values(deduplicated_data)

    def _crm_dto_from_orm(self, data: AccountORM) -> AccountDTO:
        return AccountDTO(
            id=data.id,
            account_id=data.account_id,
            account_name=data.account_name,
            industry=data.industry,
            account_value=data.account_value,
            region=RegionCRMEnum(data.region),
        )

    def _orm_from_crm_dto(self, data: AccountDTO) -> AccountORM:
        return AccountORM(
            id=data.id,
            account_id=data.account_id,
            account_name=data.account_name,
            industry=data.industry,
            account_value=data.account_value,
            region=RegionORMEnum(data.region),
        )

    def has_changes(self, crm_data: AccountDTO, db_data: AccountORM) -> bool:
        return (
            crm_data.account_id != db_data.account_id
            or crm_data.account_name != db_data.account_name
            or crm_data.industry != db_data.industry
            or crm_data.account_value != db_data.account_value
            or crm_data.region != db_data.region
        )
