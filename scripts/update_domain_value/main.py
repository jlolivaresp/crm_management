from pathlib import Path
from typing import Any, get_type_hints, get_args

import click
from dotenv import load_dotenv

from crm_management.db.utils import init_db
from crm_management.domain.accounts.crm.service import CRMAccountsAPI
from crm_management.domain.accounts.db.service import DBAccountsAPI
from crm_management.domain.accounts.service import ServiceAccount
from crm_management.domain.contacts.crm.service import CRMContactsAPI
from crm_management.domain.contacts.db.service import DBContactsAPI
from crm_management.domain.contacts.service import ServiceContact
from crm_management.domain.deals.crm.service import CRMDealsAPI
from crm_management.domain.deals.db.service import DBDealsAPI
from sqlalchemy.orm import sessionmaker

from crm_management.domain.deals.service import ServiceDeal
from crm_management.services.base import ServiceBase


THIS_FILE_PATH = Path(__file__)

DOMAIN_MAP = {
    "deals": (ServiceDeal, CRMDealsAPI, DBDealsAPI),
    "contacts": (ServiceContact, CRMContactsAPI, DBContactsAPI),
    "accounts": (ServiceAccount, CRMAccountsAPI, DBAccountsAPI)
}


def cast_to_field_type(cls: type, field_name: str, value: Any) -> Any:
    type_hints = get_type_hints(cls)

    if field_name not in type_hints:
        raise KeyError(f"Field '{field_name}' not found in class '{cls.__name__}'")

    field_type = type_hints[field_name]

    possible_types = get_args(field_type)
    if not possible_types:
        possible_types = [field_type]

    for possible_type in possible_types:
        try:
            return possible_type(value)
        except (ValueError, TypeError):
            continue

    raise TypeError(
        f"Value '{value}' could not be cast to any of the types {possible_types} for field '{field_name}'"
    )


def setup_service(service_name: str) -> ServiceBase:
    if service_name not in DOMAIN_MAP:
        raise ValueError(f"Unsupported domain: {service_name}.")

    engine = init_db()

    service, crm_api, db_api = DOMAIN_MAP[service_name]

    return service(crm_api=crm_api(), domain_api=db_api(sessionmaker(bind=engine)()))


@click.command()
@click.option(
    "--domain",
    type=click.Choice(["deals", "contacts", "accounts"], case_sensitive=False),
    required=True,
    help="Domain to update (e.g., deals).",
)
@click.option(
    "--key", type=str, required=True, help="Field to query for (e.g., deal_size)."
)
@click.option("--value", type=str, required=True, help="Value of field to query for.")
@click.option("--key-to-update", type=str, required=True, help="Old value for the field.")
@click.option("--update-value", type=str, required=True, help="New value for the field.")
def update_record(domain: str, key: str, value: Any, key_to_update: str, update_value: Any) -> None:
    service = setup_service(domain)

    key_casted_value = cast_to_field_type(service.crm_api._dto_class, key, value)
    update_key_casted_value = cast_to_field_type(service.crm_api._dto_class, key_to_update, update_value)

    crm_api_entry = service.find_by_field_name(field_name=key, value=key_casted_value)

    if not crm_api_entry:
        click.echo(f"Entity with key={key} and value={value} not found in the CRM.")
        return

    for entry in crm_api_entry:
        setattr(entry, key_to_update, update_key_casted_value)

    service.update_many(updated_data=crm_api_entry)


if __name__ == "__main__":
    load_dotenv(f"{THIS_FILE_PATH.parent.parent.parent}/.env")
    update_record()
