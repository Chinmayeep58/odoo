from pydantic import BaseModel
from typing import Optional

class TeamCreate(BaseModel):
    name: str

class TechnicianCreate(BaseModel):
    name: str
    team_id: int

class EquipmentCreate(BaseModel):
    name: str
    serial: str
    department: str
    employee: str
    location: str
    purchase_date: str
    warranty_expiry: str
    team_id: int
    default_technician: int

class RequestCreate(BaseModel):
    subject: str
    req_type: str
    equipment_id: int
    scheduled_date: Optional[str] = None

class RequestUpdate(BaseModel):
    state: Optional[str] = None
    technician_id: Optional[int] = None
    duration_hours: Optional[int] = None
