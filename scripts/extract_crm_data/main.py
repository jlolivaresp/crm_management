import os
from datetime import datetime
from pathlib import Path

import click
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from crm_management.db.utils import init_db
from crm_management.domain.accounts.crm.service import CRMAccountsAPI
from crm_management.domain.accounts.service import ServiceAccount
from crm_management.domain.contacts.crm.service import CRMContactsAPI
from crm_management.domain.contacts.db.service import DBContactsAPI
from crm_management.domain.contacts.service import ServiceContact
from crm_management.domain.deals.crm.service import CRMDealsAPI
from crm_management.domain.deals.db.service import DBDealsAPI
from crm_management.domain.accounts.db.service import DBAccountsAPI
from crm_management.domain.deals.service import ServiceDeal


THIS_FILE_PATH = Path(__file__)


@click.command()
def export_data():
    today = datetime.now().strftime("%Y-%m-%d")

    db_engine = init_db()
    session_local = sessionmaker(bind=db_engine)
    session = session_local()

    contacts_service = ServiceContact(CRMContactsAPI(), DBContactsAPI(session))
    deals_service = ServiceDeal(CRMDealsAPI(), DBDealsAPI(session))
    accounts_service = ServiceAccount(CRMAccountsAPI(), DBAccountsAPI(session))

    entities = [
        ("accounts", accounts_service),
        ("contacts", contacts_service),
        ("deals", deals_service),
    ]

    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    for entity_name, service in entities:
        data = service.find_all()

        json_filename = os.path.join(output_dir, f"{today}_{entity_name}.json")
        service.save_crm_data_to_json(json_filename, data)

        csv_filename = os.path.join(output_dir, f"{today}_{entity_name}.csv")
        service.save_crm_data_to_csv(csv_filename, data)

        print(f"Exported {entity_name} data to {json_filename} and {csv_filename}.")

        clean_data = service.clean_crm_data(data=data)

        for crm_data in clean_data:
            db_data = service.domain_api.get(id=crm_data.id)
            if db_data is None or service.has_changes(crm_data, db_data):
                service.update_one(updated_data=crm_data)

        if entity_name == "deals":
            clean_data_df = service.compute_aggregates(
                deals=clean_data, aggregation="monthly"
            )
            service.save_aggregates_to_db(
                aggregates=clean_data_df, aggregation_type="monthly"
            )

        service.update_many(updated_data=clean_data)


if __name__ == "__main__":
    load_dotenv(f"{THIS_FILE_PATH.parent.parent.parent}/.env")
    export_data()
