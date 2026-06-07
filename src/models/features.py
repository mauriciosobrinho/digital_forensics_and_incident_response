from pydantic import BaseModel


class IpFeatures(BaseModel):

    ip: str

    total_requests: int

    unique_invoice_ids: int

    requests_per_minute: float

    successful_requests: int

    failed_requests: int

    success_rate: float

    error_rate: float

    sequential_access_ratio: float

    invoice_span: int

    unique_tokens: int

    unique_user_agents: int

    active_minutes: int
