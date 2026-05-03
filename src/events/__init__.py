from dataclasses import dataclass

@dataclass
class RequestCreatedEvent:
    request_id: int
    type: str
    title: str
    owner: str
    sla_target: str