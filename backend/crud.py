from db import get_conn
from datetime import datetime

# -------- Teams --------
def create_team(name: str):
    conn = get_conn()
    conn.execute("INSERT INTO teams(name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def list_teams():
    conn = get_conn()
    data = conn.execute("SELECT * FROM teams").fetchall()
    conn.close()
    return data

# -------- Technicians --------
def create_technician(name: str, team_id: int):
    conn = get_conn()
    conn.execute(
        "INSERT INTO technicians(name, team_id) VALUES (?,?)",
        (name, team_id)
    )
    conn.commit()
    conn.close()

def list_technicians():
    conn = get_conn()
    data = conn.execute("SELECT * FROM technicians").fetchall()
    conn.close()
    return data

# -------- Equipment --------
def create_equipment(data: dict):
    conn = get_conn()
    conn.execute("""
        INSERT INTO equipment(
            name, serial, department, employee, location,
            purchase_date, warranty_expiry,
            team_id, default_technician
        )
        VALUES (?,?,?,?,?,?,?,?,?)
    """, tuple(data.values()))
    conn.commit()
    conn.close()

def list_equipment():
    conn = get_conn()
    data = conn.execute("SELECT * FROM equipment").fetchall()
    conn.close()
    return data

def mark_equipment_scrap(equipment_id: int):
    conn = get_conn()
    conn.execute(
        "UPDATE equipment SET is_scrapped=1 WHERE id=?",
        (equipment_id,)
    )
    conn.commit()
    conn.close()

# -------- Requests --------
def create_request(subject, req_type, equipment_id, scheduled_date=None):
    conn = get_conn()
    c = conn.cursor()

    team_id, tech_id = c.execute("""
        SELECT team_id, default_technician
        FROM equipment WHERE id=?
    """, (equipment_id,)).fetchone()

    c.execute("""
        INSERT INTO requests(
            subject, req_type, state,
            equipment_id, team_id, technician_id,
            scheduled_date, created_at
        )
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        subject, req_type, "New",
        equipment_id, team_id, tech_id,
        scheduled_date, datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def list_requests():
    conn = get_conn()
    data = conn.execute("SELECT * FROM requests").fetchall()
    conn.close()
    return data

def update_request(req_id: int, fields: dict):
    conn = get_conn()
    c = conn.cursor()

    for k, v in fields.items():
        c.execute(f"UPDATE requests SET {k}=? WHERE id=?", (v, req_id))

    # Scrap logic
    if fields.get("state") == "Scrap":
        c.execute("""
            UPDATE equipment SET is_scrapped=1
            WHERE id=(SELECT equipment_id FROM requests WHERE id=?)
        """, (req_id,))

    conn.commit()
    conn.close()
