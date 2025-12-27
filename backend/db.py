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
        name TEXT,
        technicians TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS equipment(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        serial TEXT,
        department TEXT,
        employee TEXT,
        team_id INTEGER
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
        technician TEXT,
        scheduled_date TEXT,
        duration_hours INTEGER
    )
    """)

    conn.commit()
    conn.close()
