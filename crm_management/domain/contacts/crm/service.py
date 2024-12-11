from crm_management.crm.service_base import CRMBaseAPI
from crm_management.domain.contacts.crm.dto import ContactDTO


class CRMContactsAPI(CRMBaseAPI[ContactDTO]):
    def __init__(self):
        super().__init__(api_endpoint="/api/contacts", dto_class=ContactDTO)

    def find_all(self) -> list[ContactDTO]:
        response = self._api_client.get(f"{self.api_endpoint}/view/202000979603").json()
        items = response.get("contacts")
        return [self._dto_class.from_dict(item) for item in items]

    def find_by_id(self, entity_id: str) -> ContactDTO:
        url = f"{self.api_endpoint}/{entity_id}"
        response = self._api_client.get(url).json()
        return self._dto_class.from_dict(response)

    def update_one(self, updated_data: ContactDTO) -> ContactDTO:
        url = f"{self.api_endpoint}/{updated_data.id}"
        response = (
            self._api_client.put(url, json=updated_data.dict()).json().get("contact")
        )
        return self._dto_class.from_dict(response)

    def delete_one(self, entity_id: str) -> bool:
        url = f"{self.api_endpoint}/{entity_id}"
        response = self._api_client.delete(url)
        return response.status_code == 204

    def create_one(self, new_data: ContactDTO) -> ContactDTO:
        response = self._api_client.post(self.api_endpoint, json=new_data.dict()).json()
        return self._dto_class.from_dict(response)
