from crm_management.crm.service_base import CRMBaseAPI
from crm_management.domain.deals.crm.dto import DealDTO


class CRMDealsAPI(CRMBaseAPI[DealDTO]):
    def __init__(self):
        super().__init__(api_endpoint="/api/deals", dto_class=DealDTO)

    def find_all(self) -> list[DealDTO]:
        response = self._api_client.get(f"{self.api_endpoint}/view/202000979613").json()
        items = response.get("deals")
        return [self._dto_class.from_dict(item) for item in items]

    def find_by_id(self, entity_id: str) -> DealDTO:
        url = f"{self.api_endpoint}/{entity_id}"
        response = self._api_client.get(url).json()
        return self._dto_class.from_dict(response)

    def update_one(self, updated_data: DealDTO) -> DealDTO:
        url = f"{self.api_endpoint}/{updated_data.id}"
        response = (
            self._api_client.put(url, json=updated_data.to_dict()).json().get("deal")
        )
        return self._dto_class.from_dict(response)

    def delete_one(self, entity_id: str) -> bool:
        url = f"{self.api_endpoint}/{entity_id}"
        response = self._api_client.delete(url)
        return response.status_code == 204

    def create_one(self, new_data: DealDTO) -> DealDTO:
        response = self._api_client.post(self.api_endpoint, json=new_data.dict()).json()
        return self._dto_class.from_dict(response)
