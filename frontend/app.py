import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(page_title="GearGuard", layout="wide")
st.title("🛠️ GearGuard — Maintenance Tracker")


# -------- Helpers --------
def get(url):
    return requests.get(f"{API}{url}").json()

def post(url, payload):
    return requests.post(f"{API}{url}", json=payload).json()

def put(url, payload):
    return requests.put(f"{API}{url}", json=payload).json()


# -------- Sidebar Creation --------
st.sidebar.header("Create Data")

with st.sidebar.expander("➕ Add Team"):
    name = st.text_input("Team Name")
    tech = st.text_input("Technicians (comma separated)")
    if st.button("Create Team"):
        post("/teams", {"name": name, "technicians": tech})
        st.success("Team created")

with st.sidebar.expander("➕ Add Equipment"):
    eq_name = st.text_input("Equipment Name")
    serial = st.text_input("Serial")
    dept = st.text_input("Department")
    emp = st.text_input("Employee")

    teams = get("/teams")
    team_map = {t[1]: t[0] for t in teams}
    team_sel = st.selectbox("Team", list(team_map.keys())) if teams else None

    if st.button("Create Equipment") and teams:
        post("/equipment", {
            "name": eq_name,
            "serial": serial,
            "department": dept,
            "employee": emp,
            "team_id": team_map[team_sel]
        })
        st.success("Equipment added")


# -------- Create Request --------
st.header("📄 Create Maintenance Request")

equipment = get("/equipment")
emap = {e[1]: e[0] for e in equipment}

col1, col2, col3 = st.columns(3)

with col1:
    subject = st.text_input("Subject")

with col2:
    rtype = st.selectbox("Type", ["Corrective", "Preventive"])

with col3:
    eq_sel = st.selectbox("Equipment", list(emap.keys())) if equipment else None

sched_date = None
if rtype == "Preventive":
    sched_date = st.date_input("Scheduled Date")

if st.button("Create Request") and equipment:
    post("/requests", {
        "subject": subject,
        "req_type": rtype,
        "equipment_id": emap[eq_sel],
        "scheduled_date": str(sched_date) if sched_date else None
    })
    st.success("Request created")


# -------- Kanban Board --------
st.header("📌 Kanban Board")

states = ["New", "In Progress", "Repaired", "Scrap"]
reqs = get("/requests")

cols = st.columns(4)

for i, state in enumerate(states):
    with cols[i]:
        st.subheader(state)

        for r in reqs:
            if r[3] == state:
                box = st.container(border=True)
                with box:
                    st.write(f"**{r[1]}**")
                    st.caption(r[2])

                    if state != "Scrap":
                        nxt = states[states.index(state) + 1]
                        if st.button(f"→ {nxt}", key=f"{r[0]}{nxt}"):
                            put(f"/requests/{r[0]}", {"state": nxt})
                            st.rerun()


# -------- Preventive Schedule --------
st.header("📅 Preventive Maintenance")

for r in reqs:
    if r[2] == "Preventive" and r[6]:
        st.write(f"• **{r[1]}** — {r[6]}")
