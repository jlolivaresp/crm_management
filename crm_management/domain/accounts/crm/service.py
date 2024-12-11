from crm_management.crm.service_base import CRMBaseAPI
from crm_management.domain.accounts.crm.dto import AccountDTO


class CRMAccountsAPI(CRMBaseAPI[AccountDTO]):
    def __init__(self):
        super().__init__(api_endpoint="/api/sales_accounts", dto_class=AccountDTO)

    def find_all(self) -> list[AccountDTO]:
        response = self._api_client.get(f"{self.api_endpoint}/view/202000979627").json()
        items = response.get("sales_accounts")
        return [self._dto_class.from_dict(item) for item in items]

    def find_by_id(self, entity_id: str) -> AccountDTO:
        url = f"{self.api_endpoint}/{entity_id}"
        response = self._api_client.get(url).json()
        return self._dto_class.from_dict(response)

    def update_one(self, updated_data: AccountDTO) -> AccountDTO:
        url = f"{self.api_endpoint}/{updated_data.id}"
        response = (
            self._api_client.put(url, json=updated_data.model_dump())
            .json()
            .get("sales_account")
        )
        return self._dto_class.from_dict(response)

    def delete_one(self, entity_id: str) -> bool:
        url = f"{self.api_endpoint}/{entity_id}"
        response = self._api_client.delete(url)
        return response.status_code == 204

    def create_one(self, new_data: AccountDTO) -> AccountDTO:
        response = self._api_client.post(self.api_endpoint, json=new_data.dict()).json()
        return self._dto_class.from_dict(response)
