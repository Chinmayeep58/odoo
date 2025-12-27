from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from db import init_db, get_conn
from schemas import *

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"msg": "GearGuard API running"}

# -------- Teams --------
@app.post("/teams")
def create_team(t: TeamCreate):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO teams(name) VALUES (?)", (t.name,))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/teams")
def list_teams():
    conn = get_conn()
    data = conn.execute("SELECT * FROM teams").fetchall()
    conn.close()
    return data

# -------- Technicians --------
@app.post("/technicians")
def create_technician(t: TechnicianCreate):
    conn = get_conn()
    conn.execute(
        "INSERT INTO technicians(name,team_id) VALUES (?,?)",
        (t.name, t.team_id)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/technicians")
def list_technicians():
    conn = get_conn()
    data = conn.execute("SELECT * FROM technicians").fetchall()
    conn.close()
    return data

# -------- Equipment --------
@app.post("/equipment")
def create_equipment(e: EquipmentCreate):
    conn = get_conn()
    conn.execute("""
        INSERT INTO equipment(
            name,serial,department,employee,location,
            purchase_date,warranty_expiry,
            team_id,default_technician
        )
        VALUES (?,?,?,?,?,?,?,?,?)
    """, tuple(e.dict().values()))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/equipment")
def list_equipment():
    conn = get_conn()
    data = conn.execute("SELECT * FROM equipment").fetchall()
    conn.close()
    return data

# -------- Requests --------
@app.post("/requests")
def create_request(r: RequestCreate):
    conn = get_conn()
    c = conn.cursor()

    eq = c.execute("""
        SELECT team_id, default_technician
        FROM equipment WHERE id=?
    """, (r.equipment_id,)).fetchone()

    c.execute("""
        INSERT INTO requests(
            subject,req_type,state,
            equipment_id,team_id,technician_id,
            scheduled_date,created_at
        )
        VALUES (?,?,?,?,?,?,?,?)
    """, (
        r.subject, r.req_type, "New",
        r.equipment_id, eq[0], eq[1],
        r.scheduled_date, datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/requests")
def list_requests():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM requests")
    data = c.fetchall()
    conn.close()
    return data

@app.put("/requests/{rid}")
def update_request(rid: int, u: RequestUpdate):
    conn = get_conn()
    c = conn.cursor()

    for k, v in u.dict(exclude_none=True).items():
        c.execute(f"UPDATE requests SET {k}=? WHERE id=?", (v, rid))

    # Scrap logic
    if u.state == "Scrap":
        c.execute("""
            UPDATE equipment SET is_scrapped=1
            WHERE id=(SELECT equipment_id FROM requests WHERE id=?)
        """, (rid,))

    conn.commit()
    conn.close()
    return {"status": "updated"}
