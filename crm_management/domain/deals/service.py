from datetime import datetime
from typing import Any, Literal

import pandas

from crm_management.domain.deals.crm.service import CRMDealsAPI
from crm_management.domain.deals.db.service import DBDealsAPI
from crm_management.domain.deals.crm.dto import DealDTO, DealStageCRMEnum
from crm_management.domain.deals.db.orm import DealORM, DealStageORMEnum
from crm_management.domain.reports.db.orm import DealAggregationORM
from crm_management.domain.reports.db.service import DBDealsAggregationAPI
from crm_management.services.base import ServiceBase


class ServiceDeal(ServiceBase[DealDTO, DealORM]):
    def __init__(self, crm_api: CRMDealsAPI, domain_api: DBDealsAPI):
        super().__init__(crm_api=crm_api, domain_api=domain_api)
        self.crm_api = crm_api
        self.domain_api = domain_api

    def find_all(self) -> list[DealDTO]:
        return super().find_all()

    def find_by_id(self, entity_id: str) -> DealDTO | None:
        return super().find_by_id(entity_id=entity_id)

    def find_by_field_name(self, field_name: str, value: Any) -> list[DealDTO]:
        return super().find_by_field_name(field_name=field_name, value=value)

    def update_one(self, updated_data: DealDTO) -> DealDTO:
        return super().update_one(updated_data=updated_data)

    def clean_crm_data(self, data: list[DealDTO]) -> list[DealDTO]:
        deduplicated_data = self._remove_duplicates(
            data=data, keys=["deal_id", "deal_name"]
        )
        return self._handle_missing_values(deduplicated_data)

    def compute_aggregates(
        self, deals: list[DealDTO], aggregation: Literal["daily", "weekly", "monthly"]
    ) -> pandas.DataFrame:
        df = self.load_to_df(data=deals)

        if "deal_size" not in df.columns or "account_id" not in df.columns:
            raise ValueError(
                "Missing required columns 'deal_size' or 'account_id' in the data."
            )

        df = df.dropna(subset=["created_at", "deal_size", "account_id"])

        if aggregation == "daily":
            df["date"] = df["created_at"].dt.date
            agg_df = (
                df.groupby(["account_id", "date"])
                .agg({"deal_size": "sum"})
                .reset_index()
            )
            agg_df.rename(
                columns={"date": "aggregation_period", "deal_size": "total_deal_size"},
                inplace=True,
            )

        elif aggregation == "weekly":
            agg_df = (
                df.groupby(["account_id", pandas.Grouper(key="created_at", freq="W")])
                .agg({"deal_size": "sum"})
                .reset_index()
            )
            agg_df.rename(
                columns={
                    "created_at": "aggregation_period",
                    "deal_size": "total_deal_size",
                },
                inplace=True,
            )

        elif aggregation == "monthly":
            agg_df = (
                df.groupby(["account_id", pandas.Grouper(key="created_at", freq="M")])
                .agg({"deal_size": "sum"})
                .reset_index()
            )
            agg_df.rename(
                columns={
                    "created_at": "aggregation_period",
                    "deal_size": "total_deal_size",
                },
                inplace=True,
            )

        else:
            raise ValueError(
                "Invalid aggregation level. Choose from 'daily', 'weekly', or 'monthly'."
            )

        return agg_df

    def save_aggregates_to_db(
        self, aggregates: pandas.DataFrame, aggregation_type: str
    ) -> None:
        if aggregation_type not in {"daily", "weekly", "monthly"}:
            raise ValueError(
                "Invalid aggregation type. Must be 'daily', 'weekly', or 'monthly'."
            )

        deal_aggregations = [
            DealAggregationORM(
                account_id=row["account_id"],
                aggregation_type=aggregation_type,
                aggregation_date=(
                    row["aggregation_period"].date()
                    if isinstance(row["aggregation_period"], pandas.Timestamp)
                    else datetime.strptime(
                        str(row["aggregation_period"]).split(" ")[0], "%Y-%m-%d"
                    ).date()
                ),
                total_deal_size=row["total_deal_size"],
                deal_count=row.get("deal_count", 0),
            )
            for _, row in aggregates.iterrows()
        ]

        deals_agg_service = DBDealsAggregationAPI(session=self.domain_api.session)
        for deal_agg in deal_aggregations:
            existing_record = deals_agg_service.find_by_fields(
                account_id=deal_agg.account_id,
                aggregation_type=deal_agg.aggregation_type,
                aggregation_date=deal_agg.aggregation_date,
            )
            if existing_record:
                existing_record.total_deal_size = deal_agg.total_deal_size
                existing_record.deal_count = deal_agg.deal_count
                deals_agg_service.update(id=existing_record.id, updates=existing_record)
            else:
                deals_agg_service.create(deal_agg)

    def _crm_dto_from_orm(self, data: DealORM) -> DealDTO:
        return DealDTO(
            id=data.id,
            deal_id=data.deal_id,
            deal_name=data.deal_name,
            deal_size=data.deal_size,
            probability_of_closure=data.probability_of_closure,
            deal_stage=DealStageCRMEnum(data.deal_stage),
            account_id=data.account_id,
            created_at=data.created_at,
        )

    def _orm_from_crm_dto(self, data: DealDTO) -> DealORM:
        return DealORM(
            id=data.id,
            deal_id=data.deal_id,
            deal_name=data.deal_name,
            deal_size=data.deal_size,
            probability_of_closure=data.probability_of_closure,
            deal_stage=DealStageORMEnum(data.deal_stage),
            account_id=data.account_id,
            created_at=data.created_at,
        )

    def has_changes(self, crm_data: DealDTO, db_data: DealORM) -> bool:
        return (
            crm_data.deal_id != db_data.deal_id
            or crm_data.deal_name != db_data.deal_name
            or crm_data.deal_size != db_data.deal_size
            or crm_data.probability_of_closure != db_data.probability_of_closure
            or crm_data.deal_stage != db_data.deal_stage
            or crm_data.account_id != db_data.account_id
            or crm_data.created_at != db_data.created_at
        )
