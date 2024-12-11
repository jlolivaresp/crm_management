# CRM Management

## Application Directory Structure and Domain-Based Architecture

### Overview

This application follows a **Domain-Driven Design (DDD)** approach, where each domain is represented by its own folder. Each domain contains components to interact with external services (CRM APIs) and internal databases, and it provides the necessary services for that domain's operations.

In this structure, the application is split into several key areas:

- **CRM**: For data integration with external CRM systems.
- **DB**: For internal database operations and interactions.
- **Domain**: The core of the application where domain logic resides. Each domain folder encapsulates logic for a specific business entity (e.g., Accounts, Contacts, Deals).

### Core Principles
- **Separation of Concerns**: Each domain is self-contained and follows a consistent structure, making it easy to extend the application by adding new domains.
- **Service Layer**: Each domain has a service layer to provide an entry point for business logic.
- **DTO and ORM**: Each domain uses Data Transfer Objects (DTOs) to communicate data and ORM models to persist data in the internal database.

### Directory Structure

#### Root Directory

```plaintext
app
├── crm
├── db
├── domain
├── services
```

1. **`crm/`**: This directory is responsible for interacting with the external CRM API to fetch and send data. It includes configuration files, base logic for communication with the CRM, and service files for domain-specific operations.
   
2. **`db/`**: This directory holds files related to database operations, including ORM models and database service layers for querying, updating, and deleting records.

3. **`domain/`**: This is the core directory of the application, containing business logic for each domain (e.g., Accounts, Contacts, Deals). It is organized by individual domains, each with its own subfolders for CRM integration, database interactions, and service layer.

4. **`services/`**: This directory contains base services and helper functions shared across multiple domains.

---

#### `crm/` Directory

This directory defines the components that handle interaction with the external CRM API. The files here should provide mechanisms to fetch, manipulate, and synchronize data between the CRM system and the application.

```plaintext
crm
├── client_base.py    # Base class to interact with the CRM API
├── config.py         # Configuration file for CRM integration
├── dto_base.py       # Base class for DTOs (Data Transfer Objects)
├── service_base.py   # Base services to be extended by domain-specific services
```

- **`client_base.py`**: Contains base logic for CRM API communication (e.g., authentication, making API requests).
- **`config.py`**: Configuration file that holds the necessary credentials, endpoints, and API settings.
- **`dto_base.py`**: Contains base DTO logic, which is extended by the domain-specific DTOs.
- **`service_base.py`**: Contains base services that handle CRM-related operations common across domains (e.g., fetching data from the CRM).

#### `db/` Directory

This directory holds components that manage the interactions with the internal database. This includes SQLAlchemy ORM models, database service layers, and utility files for database-related operations.

```plaintext
db
├── orm_base.py       # Base ORM models for interacting with the database
├── service_base.py   # Base services for database operations
├── utils.py          # Utility functions for the database
```

- **`orm_base.py`**: Contains the base ORM models that represent the internal database schema. These models will be extended by domain-specific ORM models.
- **`service_base.py`**: Base services that handle database operations like CRUD (Create, Read, Update, Delete) and querying.
- **`utils.py`**: Helper functions for database interactions (e.g., session management, querying helpers).

#### `domain/` Directory

This is the core directory where each domain resides. For example, the `accounts`, `contacts`, and `deals` domains will each have their own folder under the `domain/` directory.

```plaintext
domain
├── accounts
│   ├── crm
│   ├── db
│   ├── service.py
├── contacts
│   ├── crm
│   ├── db
│   ├── service.py
├── deals
│   ├── crm
│   ├── db
│   ├── service.py
├── reports
│   ├── db
│   ├── service.py
```

For each domain (e.g., `accounts`, `contacts`, `deals`), you might find:

- **`crm/`**: Contains domain-specific logic for interacting with the CRM API. This includes fetching or syncing domain-specific data (e.g., contacts, accounts) with the CRM.
- **`db/`**: Contains ORM models and database logic specific to that domain, responsible for persisting data in the internal database.
- **`service.py`**: Contains the domain-specific service logic that acts as an entry point for business operations. It combines CRM and DB operations.

#### Example: Account Domain

```plaintext
domain/accounts
├── crm
│   ├── dto.py           # DTO for data transfer related to accounts
│   ├── service.py       # CRM-specific logic for accounts
├── db
│   ├── orm.py           # ORM model for the accounts table
│   ├── service.py       # DB service logic for accounts (CRUD operations)
└── service.py           # Business logic for accounts (combines CRM and DB logic)
```

1. **`crm/dto.py`**: Defines the Data Transfer Object (DTO) for accounts. DTOs are used to transform data between the external CRM system and the internal application.
2. **`crm/service.py`**: Handles CRM-specific logic for accounts, like fetching or updating account data from the CRM system.
3. **`db/orm.py`**: Defines the ORM model for the accounts table in the internal database.
4. **`db/service.py`**: Provides CRUD operations for interacting with the `accounts` table in the database.
5. **`service.py`**: Combines CRM and DB logic to provide business services for the account domain, such as creating, updating, or retrieving accounts.

### Adding New Domains

To add a new domain, follow this pattern:

1. Create a new folder under `domain/` (e.g., `domain/<new_domain>`).
2. If applies, add the necessary files under the `crm/` subfolder to integrate with the external CRM API (e.g., `dto.py` and `service.py`).
3. If applies, create the ORM model under `db/` with the necessary database schema in `orm.py`.
4. If applies, implement the database interaction logic in `db/service.py` using SQLAlchemy (for CRUD operations).
5. Add the necessary business logic in `service.py`, combining both CRM and DB services (if applies) to perform the domain's operations.

### Example: Adding a New "Products" Domain

To add a "Products" domain:

```plaintext
domain/products
├── crm
│   ├── dto.py           # DTO for products data from the CRM
│   ├── service.py       # Logic to fetch products data from the CRM
├── db
│   ├── orm.py           # ORM model for the products table in the DB
│   ├── service.py       # CRUD operations for products
└── service.py           # Business logic for managing products (CRM + DB)
```

---

## Usage Example

In this section, we provide an example of how to use the services in the application, focusing on how to interact with the CRM API, DB API, and perform the necessary operations such as CRUD and data cleaning.

### Service Base

The base service, `ServiceBase`, abstracts the logic for interacting with the CRM API and the database (DB) API. It provides several common methods that can be reused across different domains.

The following methods are available in the base service:

- **save_crm_data_to_json**: Saves CRM data to a JSON file.
- **save_crm_data_to_csv**: Saves CRM data to a CSV file.
- **find_all**: Retrieves all data from the CRM.
- **find_by_id**: Finds a record in the CRM by its ID.
- **find_by_field_name**: Finds records by a specific field and value.
- **update_one**: Updates a single record in the DB, or creates it if it doesn't exist.
- **update_many**: Updates multiple records.
- **clean_crm_data**: A method for cleaning and transforming CRM data.
- **load_to_df**: Loads data into a pandas DataFrame.
- **_remove_duplicates**: Removes duplicate records based on specific fields.
- **_handle_missing_values**: Handles missing values in the data.
- **_crm_dto_from_orm**: Converts ORM instance to CRM DTO.
- **_orm_from_crm_dto**: Converts CRM DTO to ORM instance.

### Example Usage of `ServiceAccount`

The `ServiceAccount` class demonstrates how a domain-specific service is built by inheriting from the `ServiceBase` class. It integrates the `CRMAccountsAPI` (CRM API) and `DBAccountsAPI` (DB API) to manage account-related data. Below is an example of how to use `ServiceAccount`:

```python
from sqlalchemy.orm import sessionmaker

from crm_management.db.utils import init_db
from crm_management.domain.accounts.service import ServiceAccount
from crm_management.domain.accounts.crm.service import CRMAccountsAPI
from crm_management.domain.accounts.db.service import DBAccountsAPI
from crm_management.domain.accounts.crm.dto import AccountDTO, RegionCRMEnum
from crm_management.domain.accounts.db.orm import AccountORM, RegionORMEnum

engine = init_db()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create instances of CRM API and DB API
crm_api = CRMAccountsAPI()
domain_api = DBAccountsAPI(session)

# Initialize the service for managing accounts
account_service = ServiceAccount(crm_api=crm_api, domain_api=domain_api)

# Example: Find all accounts
accounts = account_service.find_all()
print("All accounts:", accounts)

# Example: Find an account by ID
account_id = "12345"
account = account_service.find_by_id(account_id)
print(f"Account with ID {account_id}: {account}")

# Example: Find accounts by field name
accounts_with_name = account_service.find_by_field_name("account_name", "Acme Corp")
print("Accounts with name 'Acme Corp':", accounts_with_name)

# Example: Update an account (if it exists in DB)
updated_account_data = AccountDTO(
    id=1,
    account_id=123,
    account_name="Updated Account",
    industry="Tech",
    account_value=500000,
    region=RegionCRMEnum.NORTH_AMERICA
)
updated_account = account_service.update_one(updated_data=updated_account_data)
print("Updated account:", updated_account)

# Example: Update multiple accounts
updated_accounts_data = [
    AccountDTO(
        id=2,
        account_id=124,
        account_name="Another Account",
        industry="Retail",
        account_value=750000,
        region=RegionCRMEnum.EUROPE
    ),
    AccountDTO(
        id=3,
        account_id=125,
        account_name="New Account",
        industry="Finance",
        account_value=1000000,
        region=RegionCRMEnum.ASIA
    )
]
updated_accounts = account_service.update_many(updated_data=updated_accounts_data)
print("Updated accounts:", updated_accounts)

# Example: Clean CRM data
cleaned_accounts = account_service.clean_crm_data(data=accounts)
print("Cleaned accounts:", cleaned_accounts)

# Example: Save CRM data to JSON file
account_service.save_crm_data_to_json(output_path="accounts_data.json", crm_data=accounts)

# Example: Save CRM data to CSV file
account_service.save_crm_data_to_csv(output_path="accounts_data.csv", crm_data=accounts)
```

---

## Environment variables
For demonstration purposes, the current code uses an .env file to parse environment variables required for the code to run, like the Database URL and the API token, 
however, in an environment production, these should not be written to any files but provided via secrets to the code.

---

## `scripts/` Documentation

Scripts are organized by folders inside the `scripts` folder. Each should have its own main.py being a cli tool that can 
be executed by running a docker container and providing the path of the script to the `docker run` command, 
ensuring that the environment is consistent across different setups and scripts.

Before running any scripts, make sure to build the docker image. This can be accomplished by using the `build_docker_image.sh` script.

### `scripts/extract_crm_data`

This folder contains the necessary scripts to extract data from the CRM APIs, process it, and save it in different formats. Below is an overview of the folder structure and how the various scripts work together.

#### Folder Structure

```
scripts/
└── extract_crm_data
    ├── configure_cronjob.sh
    ├── main.py
    └── run_main_cli.sh
```

- **`configure_cronjob.sh`**: This script is used to configure a cron job that can run the `main.py` script periodically, automating the process of extracting CRM data. Make sure to specify the output oath that you'd like to output the files to.

- **`main.py`**: The core script for extracting data from the CRM, cleaning it, and saving it to both JSON and CSV formats. It utilizes the application's services to interact with the CRM and the database.

- **`run_main_cli.sh`**: A shell script to run the `main.py` script as a CLI command, making it easier to execute the extraction process manually or through automation. This script accepts 1 argument and that is the output folder where you'd like to store the extracted results.

#### Usage

To run the script, execute it with the required parameters:
```bash
scripts/extract_crm_data/run_main_cli.sh <YOUR OUTPUT PATH>
```

### `scripts/update_domain_value`

This script provides a command-line interface (CLI) tool to update records in a CRM system. The script supports operations across multiple domains (e.g., deals, contacts, accounts) and ensures proper type handling when querying and updating fields.

#### Features

- Domain Selection: Choose between deals, contacts, or accounts.
- Type-Safe Casting: Automatically cast query and update values to the correct type based on the domain's Data Transfer Object (DTO) definitions.
- Batch Updates: Supports updating multiple records in one operation.
- Error Handling: Provides clear feedback if fields or records are not found or if type casting fails.

#### Usage

To run the script, execute it with the required parameters:

```bash
scripts/update_domain_value/run_main_cli.sh \
    --domain deals \
    --key deal_id \
    --value 203 \
    --key-to-update deal_size \
    --update-value 24456
```

---

## Database Schema Design for CRM System

### Tables Overview

#### 1. **Accounts Table**
- **Schema:**
  ```sql
  CREATE TABLE accounts (
      id SERIAL PRIMARY KEY,
      account_id INTEGER UNIQUE NOT NULL,
      account_name VARCHAR NOT NULL,
      industry VARCHAR NOT NULL,
      account_value INTEGER NOT NULL,
      region ENUM('North America', 'Europe', 'Asia') NOT NULL
  );
  ```
- **Description:** 
  The `accounts` table stores information about customers' organizations. Each row represents a unique account, with fields such as account name, industry, and region.

- **Relationships:** 
  - `accounts` is related to the `deals` table via a foreign key (`account_id`).

#### 2. **Contacts Table**
- **Schema:**
  ```sql
  CREATE TABLE contacts (
      id SERIAL PRIMARY KEY,
      contact_id VARCHAR UNIQUE NOT NULL,
      first_name VARCHAR NOT NULL,
      last_name VARCHAR NOT NULL,
      email VARCHAR NOT NULL,
      job_title VARCHAR,
      lead_source ENUM('Website', 'Referral', 'Email Campaign') NOT NULL,
      last_contact_date DATE
  );
  ```
- **Description:** 
  The `contacts` table represents individuals who work for the accounts stored in the CRM. Each record includes personal details such as name, email, and the lead source.

- **Relationships:** 
  - The `contacts` table does not have a direct relationship with other tables but is logically linked to accounts by association.

#### 3. **Deals Table**
- **Schema:**
  ```sql
  CREATE TABLE deals (
      id SERIAL PRIMARY KEY,
      deal_id INTEGER UNIQUE NOT NULL,
      deal_name VARCHAR NOT NULL,
      deal_size INTEGER,
      probability_of_closure VARCHAR NOT NULL,
      deal_stage ENUM('Prospecting', 'Negotiation', 'Closed-Won', 'Closed-Lost') NOT NULL,
      account_id INTEGER NOT NULL REFERENCES accounts(account_id),
      created_at TIMESTAMP NOT NULL
  );
  ```
- **Description:** 
  The `deals` table tracks opportunities related to each account. Fields include the deal name, size, stage (e.g., `Closed-Won` or `Prospecting`), and the associated account.

- **Relationships:** 
  - The `account_id` field creates a foreign key relationship with the `accounts` table. Each deal must belong to a valid account.

#### 4. **Deal Aggregations Table**
- **Schema:**
  ```sql
  CREATE TABLE deal_aggregations (
      id SERIAL PRIMARY KEY,
      account_id INTEGER NOT NULL REFERENCES accounts(account_id),
      aggregation_type VARCHAR NOT NULL,
      aggregation_date DATE NOT NULL,
      total_deal_size FLOAT NOT NULL,
      deal_count INTEGER NOT NULL
  );
  ```
- **Description:** 
  The `deal_aggregations` table stores aggregated data, such as the total size of deals and the number of deals for each account, grouped by aggregation type (e.g., daily, weekly, monthly).

- **Relationships:** 
  - `deal_aggregations` is directly linked to the `accounts` table via the `account_id` foreign key.

### Key Assumptions

1. **Account Region and Industry:** 
   - Each account is associated with a specific region (`North America`, `Europe`, or `Asia`) and an industry type, which helps segment accounts for reporting and analytics.

2. **Unique Identifiers:**
   - `account_id`, `contact_id`, and `deal_id` are unique within their respective tables to ensure that no duplicate records exist.
   - Relationships between tables use these identifiers rather than the primary key (`id`) to ensure consistency with CRM standards.

3. **Enum Fields:**
   - Fields like `region`, `lead_source`, and `deal_stage` use enums to constrain the data and ensure only valid values are stored.

4. **Timestamped Deals:**
   - Deals must include a `created_at` timestamp, which allows for temporal analysis and aggregation (e.g., total deal sizes by month).

5. **Optional Fields:**
   - Some fields, such as `deal_size` in the `deals` table and `job_title` in the `contacts` table, are nullable because they may not always be available during record creation.

6. **Aggregation Types:**
   - The `aggregation_type` in `deal_aggregations` specifies the period (e.g., daily, weekly, or monthly) over which the deals were grouped.

### Relationships to CRM Records

1. **Accounts Table:**
   - Directly maps to the `AccountDTO` in the CRM system.
   - `RegionCRMEnum` maps to the `region` enum field in the database.

2. **Contacts Table:**
   - Directly corresponds to the `ContactDTO`.
   - The `lead_source` enum field in the database aligns with `LeadSourceCRMEnum`.

3. **Deals Table:**
   - Directly corresponds to the `DealDTO`.
   - The `deal_stage` enum field in the database aligns with `DealStageCRMEnum`.
   - The `account_id` field ties deals to accounts, ensuring that each deal is associated with a valid customer organization.

4. **Deal Aggregations Table:**
   - Stores computed results derived from the `deals` table. These computations include total deal size and count per account, grouped by a specific time period (daily, weekly, or monthly).

### Other SQL queries involved

In this case we do not use direct SQL queries as this is error prone and results in huge string concatenations and formatting.
For this purpose we used SQLAlchemy for data querying and updates and inserts and pandas for data manipulation. 
However, below are some queries that could represent the operations performed.


- **Finding All Records**:

In the code, the find_all() methods of ServiceContact, ServiceDeal, and ServiceAccount use their respective ORM services (DBContactsAPI, DBDealsAPI, DBAccountsAPI) to retrieve all records from the database.

```sql
SELECT * FROM <table_name>;
```

- **Finding by ID**:

The find_by_id() method fetches specific records based on the primary key.

```sql
SELECT * FROM <table_name> WHERE id = <entity_id>;
```

- **Finding by Field Name**:

Used when searching by other fields.

```sql
SELECT * FROM <table_name> WHERE <field_name> = <value>;
```

#### Data Updates and Inserts

- **Check if a Record Exists**:

```sql
SELECT * FROM <table_name> WHERE id = <entity_id>;
```

- **Update a Record**:

The update_one() method updates the record if it already exists.

```sql
UPDATE <table_name>
SET column1 = value1, column2 = value2, ...
WHERE id = <entity_id>;
```

- **Insert a New Record**:

```sql
INSERT INTO <table_name> (column1, column2, ...)
VALUES (value1, value2, ...);
```

#### Data Aggregation
When computing deal aggregates in the compute_aggregates() method, SQL queries similar to the following are executed:

- **Daily Aggregates**:

```sql
SELECT account_id, DATE(created_at) AS aggregation_period, SUM(deal_size) AS total_deal_size
FROM deals
WHERE created_at IS NOT NULL AND deal_size IS NOT NULL
GROUP BY account_id, DATE(created_at);
```
- **Weekly Aggregates**:

```sql
SELECT account_id, DATE_TRUNC('week', created_at) AS aggregation_period, SUM(deal_size) AS total_deal_size
FROM deals
WHERE created_at IS NOT NULL AND deal_size IS NOT NULL
GROUP BY account_id, DATE_TRUNC('week', created_at);
```

- **Monthly Aggregates**:

```sql
SELECT account_id, DATE_TRUNC('month', created_at) AS aggregation_period, SUM(deal_size) AS total_deal_size
FROM deals
WHERE created_at IS NOT NULL AND deal_size IS NOT NULL
GROUP BY account_id, DATE_TRUNC('month', created_at);
```

#### Save Aggregates to Database

```sql
SELECT * FROM deal_aggregations
WHERE account_id = <account_id>
  AND aggregation_type = <aggregation_type>
  AND aggregation_date = <aggregation_date>;
```

- **Update Aggregation Record**:

```sql
UPDATE deal_aggregations
SET total_deal_size = <new_total>, deal_count = <new_count>
WHERE id = <aggregation_id>;
```

- **Insert Aggregation Record**:

```sql
INSERT INTO deal_aggregations (account_id, aggregation_type, aggregation_date, total_deal_size, deal_count)
VALUES (<account_id>, <aggregation_type>, <aggregation_date>, <total_deal_size>, <deal_count>);
```

#### Data Cleaning and Deduplication

- **Remove Duplicates**: 
Depending on the deduplication logic (e.g., identifying unique rows based on keys like deal_id and deal_name), SQL queries like the following might be executed:

```sql
SELECT DISTINCT ON (deal_id, deal_name) *
FROM deals;
```

- **Handle missing values**:
Rows with missing values in specific columns (deal_size, account_id, etc.) are dropped.

```sql
SELECT *
FROM deals
WHERE deal_size IS NOT NULL AND account_id IS NOT NULL;
```

#### Combined Queries
Some operations combine multiple queries, for example:

- **Check if a record exists, then update it if necessary, otherwise insert it**:
```sql
WITH upsert AS (
  UPDATE <table_name>
  SET column1 = value1, column2 = value2, ...
  WHERE id = <entity_id>
  RETURNING *
)
INSERT INTO <table_name> (column1, column2, ...)
SELECT value1, value2, ...
WHERE NOT EXISTS (SELECT * FROM upsert);
```

---

## Potential Improvements

- Better error handling
- Add logging
- Fixing typing errors
- Split repository into versioned crm_management library and scripts
- Configure secrets with sensitive data like API tokens and database URLs, and providing these to the docker run command.