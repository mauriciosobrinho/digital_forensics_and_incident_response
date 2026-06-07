from datetime import datetime

from pydantic import BaseModel


class ParsedEvent(BaseModel):

    timestamp: datetime

    source_ip: str

    status_code: int

    host: str

    method: str

    referer: str

    user_agent: str

    invoice_id: int | None = None

    site_id: str | None = None

    auth_token: str | None = None
