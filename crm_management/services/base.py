import csv
import json
from abc import abstractmethod
from typing import Generic, TypeVar, Type, Any

import pandas

from crm_management.crm.dto_base import BaseDTO
from crm_management.crm.service_base import CRMBaseAPI
from crm_management.db.orm_base import Base
from crm_management.db.service_base import DBBaseAPI

T = TypeVar("T", bound=BaseDTO)
V = TypeVar("V", bound=Base)


class ServiceBase(Generic[T, V]):
    def __init__(self, crm_api: CRMBaseAPI, domain_api: DBBaseAPI):
        self.crm_api = crm_api
        self.domain_api = domain_api

    @staticmethod
    def save_crm_data_to_json(output_path: str, crm_data: list[T]) -> None:
        with open(output_path, "w") as json_file:
            json_strings = [model.model_dump_json() for model in crm_data]
            data = [json.loads(json_str) for json_str in json_strings]
            json.dump(data, json_file, indent=4)

    @staticmethod
    def save_crm_data_to_csv(output_path: str, crm_data: list[T]) -> None:
        if len(crm_data) == 0:
            raise ValueError("crm_data is empty.")

        field_names = crm_data[0].dict().keys()

        with open(output_path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for model in crm_data:
                writer.writerow(model.dict())

    def find_all(self) -> list[T]:
        return self.crm_api.find_all()

    def find_by_id(self, entity_id: str) -> T | None:
        return self.crm_api.find_by_id(entity_id=entity_id)

    def find_by_field_name(self, field_name: str, value: Any) -> list[T]:
        results: list[T] = []
        for item in self.find_all():
            if getattr(item, field_name) == value:
                results.append(item)

        return results

    def update_one(self, updated_data: T) -> T:
        entity_exists = self.domain_api.get(id=updated_data.id)
        orm_instance = self._orm_from_crm_dto(updated_data)
        if entity_exists:
            self.domain_api.update(id=updated_data.id, updates=orm_instance)
        else:
            self.domain_api.create(orm_instance)
        return self.crm_api.update_one(updated_data=updated_data)

    def update_many(self, updated_data: list[T]) -> list[T]:
        for data in updated_data:
            self.update_one(updated_data=data)
        return updated_data

    @abstractmethod
    def clean_crm_data(self, data: list[T]) -> list[T]:
        pass

    @staticmethod
    def load_to_df(data: list[T]) -> pandas.DataFrame:
        data = [deal.dict() for deal in data]
        return pandas.DataFrame(data)

    def _remove_duplicates(self, data: list[T], keys: list[str]) -> list[T]:
        df = self.load_to_df(data=data)

        df_unique = df.drop_duplicates(subset=keys)

        unique_dtos = [
            self.crm_api._dto_class.parse_obj(row)
            for row in df_unique.to_dict(orient="records")
        ]

        return unique_dtos

    def _handle_missing_values(self, data: list[T]) -> list[T]:
        return data

    @abstractmethod
    def _crm_dto_from_orm(self, data: T) -> V:
        pass

    @abstractmethod
    def _orm_from_crm_dto(self, data: V) -> T:
        pass

    @abstractmethod
    def has_changes(self, crm_data: T, db_data: V):
        pass
