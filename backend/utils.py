from datetime import date, datetime

VALID_STATES = ["New", "In Progress", "Repaired", "Scrap"]

def validate_state_transition(old, new):
    order = VALID_STATES
    return order.index(new) >= order.index(old)

def is_overdue(scheduled_date: str):
    if not scheduled_date:
        return False
    return date.fromisoformat(scheduled_date) < date.today()

def format_date(d: str):
    return datetime.fromisoformat(d).strftime("%d %b %Y")

def auto_assign_technician(equipment_row):
    # fallback logic if no default technician
    return equipment_row[8] if equipment_row[8] else None
