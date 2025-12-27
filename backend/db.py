import sqlite3

DB_NAME = "gearguard.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS teams(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS technicians(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        team_id INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS equipment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        serial TEXT,
        department TEXT,
        employee TEXT,
        location TEXT,
        purchase_date TEXT,
        warranty_expiry TEXT,
        team_id INTEGER,
        default_technician INTEGER,
        is_scrapped INTEGER DEFAULT 0
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        req_type TEXT,
        state TEXT,
        equipment_id INTEGER,
        team_id INTEGER,
        technician_id INTEGER,
        scheduled_date TEXT,
        duration_hours INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()
