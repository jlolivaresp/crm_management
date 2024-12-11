from dataclasses import dataclass


@dataclass
class APIConfig:
    BASE_URL: str = "https://sbtitest-org.myfreshworks.com/crm/sales"
