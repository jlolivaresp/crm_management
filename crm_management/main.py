from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crm_management.db.orm_base import Base
from crm_management.domain.deals.crm.service import CRMDealsAPI
from crm_management.domain.deals.db.service import DBDealsAPI
from crm_management.domain.deals.db.orm import DealORM
from crm_management.domain.deals.service import ServiceDeal

load_dotenv("/crm_management/.env")

if __name__ == "__main__":
    # service_account = ServiceAccount(crm_api=CRMAccountsAPI(), domain_api=DBAccountsAPI(None))
    # data = service_account.find_all()
    # service_account.save_crm_data_to_json("/home/jorge/jorge/crm_management/accounts.json", data)
    # service_account.save_crm_data_to_csv("/home/jorge/jorge/crm_management/accounts.csv", data)
    #
    # service_contact = ServiceContact(crm_api=CRMContactsAPI(), domain_api=DBContactsAPI(None))
    # data = service_contact.find_all()
    # service_contact.save_crm_data_to_json("/home/jorge/jorge/crm_management/contacts.json", data)
    # service_contact.save_crm_data_to_csv("/home/jorge/jorge/crm_management/contacts.csv", data)

    service_deals = ServiceDeal(crm_api=CRMDealsAPI(), domain_api=DBDealsAPI(None))
    all_deals = service_deals.find_all()
    # service_deals.save_crm_data_to_json("/home/jorge/jorge/crm_management/deals.json", all_deals)
    # service_deals.save_crm_data_to_csv("/home/jorge/jorge/crm_management/deals.csv", all_deals)

    # deal_to_update = service_deals.find_by_field_name(field_name="deal_id", value=203)
    # result_df = service_deals.compute_aggregates(all_deals, "daily")
    # deal_to_update[0].deal_size = 30000
    #
    # updated_data = service_deals.update_one(updated_data=deal_to_update[0])

    DATABASE_URL = "sqlite:///example.db"  # Replace with your DB URL

    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    Base.metadata.create_all(engine)

    for deal_dto in all_deals:
        deal = DealORM(
            deal_id=deal_dto.deal_id,
            deal_name=deal_dto.deal_name,
            deal_size=deal_dto.deal_size,
            probability_of_closure=deal_dto.probability_of_closure,
            deal_stage=deal_dto.deal_stage,
            account_id=deal_dto.account_id,
            created_at=deal_dto.created_at,
        )
        session.add(deal)
    session.commit()
