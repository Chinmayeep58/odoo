from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from db import init_db, get_conn

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Streamlit access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TeamCreate(BaseModel):
    name: str
    technicians: str


class EquipmentCreate(BaseModel):
    name: str
    serial: str
    department: str
    employee: str
    team_id: int


class RequestCreate(BaseModel):
    subject: str
    req_type: str
    equipment_id: int
    scheduled_date: Optional[str] = None


class RequestUpdate(BaseModel):
    state: Optional[str] = None
    technician: Optional[str] = None
    duration_hours: Optional[int] = None


@app.get("/")
def root():
    return {"msg": "GearGuard API running"}


# ------- Teams -------
@app.post("/teams")
def create_team(team: TeamCreate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO teams(name, technicians) VALUES (?,?)",
                (team.name, team.technicians))
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/teams")
def list_teams():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM teams")
    data = cur.fetchall()
    conn.close()
    return data


# ------- Equipment -------
@app.post("/equipment")
def create_equipment(eq: EquipmentCreate):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO equipment(name,serial,department,employee,team_id)
        VALUES (?,?,?,?,?)
    """, (eq.name, eq.serial, eq.department, eq.employee, eq.team_id))
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/equipment")
def list_equipment():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM equipment")
    data = cur.fetchall()
    conn.close()
    return data


# ------- Requests -------
@app.post("/requests")
def create_request(req: RequestCreate):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT team_id FROM equipment WHERE id=?", (req.equipment_id,))
    team = cur.fetchone()

    cur.execute("""
        INSERT INTO requests(subject,req_type,state,equipment_id,team_id,scheduled_date)
        VALUES (?,?,?,?,?,?)
    """, (req.subject, req.req_type, "New", req.equipment_id, team[0], req.scheduled_date))

    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/requests")
def list_requests():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM requests")
    data = cur.fetchall()
    conn.close()
    return data


@app.put("/requests/{req_id}")
def update_request(req_id: int, data: RequestUpdate):
    conn = get_conn()
    cur = conn.cursor()

    if data.state:
        cur.execute("UPDATE requests SET state=? WHERE id=?", (data.state, req_id))

    if data.technician:
        cur.execute("UPDATE requests SET technician=? WHERE id=?", (data.technician, req_id))

    if data.duration_hours:
        cur.execute("UPDATE requests SET duration_hours=? WHERE id=?", (data.duration_hours, req_id))

    conn.commit()
    conn.close()
    return {"status": "updated"}
