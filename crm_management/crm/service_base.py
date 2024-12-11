import os
from abc import abstractmethod
from typing import TypeVar, Generic, Type

from crm_management.crm.client_base import APIClient
from crm_management.crm.config import APIConfig
from crm_management.crm.dto_base import BaseDTO

T = TypeVar("T", bound=BaseDTO)


class CRMBaseAPI(Generic[T]):
    def __init__(self, api_endpoint: str, dto_class: Type[T]):
        self.api_endpoint = api_endpoint
        self._dto_class: Type[T] = dto_class
        self.__api_client: APIClient | None = None

    @property
    def _api_client(self) -> APIClient:
        if self.__api_client is None:
            self.__api_client = APIClient(
                base_url=APIConfig.BASE_URL,
                headers={
                    "Authorization": f"Token token={os.getenv('CRM_API_TOKEN')}",
                    "Content-Type": "application/json",
                },
            )
        return self.__api_client

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: str) -> T:
        pass

    @abstractmethod
    def update_one(self, updated_data: T) -> T:
        pass

    @abstractmethod
    def delete_one(self, entity_id: str) -> bool:
        pass

    @abstractmethod
    def create_one(self, new_data: T) -> T:
        pass
