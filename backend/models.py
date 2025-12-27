from dataclasses import dataclass
from typing import Optional

@dataclass
class Team:
    id: int
    name: str

@dataclass
class Technician:
    id: int
    name: str
    team_id: int

@dataclass
class Equipment:
    id: int
    name: str
    serial: str
    department: str
    employee: str
    location: str
    purchase_date: str
    warranty_expiry: str
    team_id: int
    default_technician: int
    is_scrapped: int

@dataclass
class Request:
    id: int
    subject: str
    req_type: str
    state: str
    equipment_id: int
    team_id: int
    technician_id: Optional[int]
    scheduled_date: Optional[str]
    duration_hours: Optional[int]
    created_at: str
