from datetime import datetime

from pydantic import BaseModel


class BaseDTO(BaseModel):
    id: int

    class Config:
        use_enum_values = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}
