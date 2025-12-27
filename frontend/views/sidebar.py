import streamlit as st
import requests

API = "http://localhost:8000"


# ---------------- SAFE HTTP HELPERS ----------------
def get(u):
    r = requests.get(API + u)
    if r.status_code != 200:
        st.error(f"GET {u} failed: {r.text}")
        return []
    return r.json()

def post(u, p):
    r = requests.post(API + u, json=p)
    if r.status_code != 200:
        st.error(f"POST {u} failed: {r.text}")
        return None
    return r.json()


# ---------------- SIDEBAR ----------------
def sidebar():
    st.sidebar.header("⚙️ Configuration")

    # ---------- Add Team ----------
    with st.sidebar.expander("➕ Add Team"):
        name = st.text_input("Team Name", key="team_name")

        if st.button("Create Team"):
            if not name:
                st.warning("Team name is required")
            else:
                post("/teams", {"name": name})
                st.success("Team created")
                st.rerun()

    # ---------- Add Technician ----------
    with st.sidebar.expander("➕ Add Technician"):
        teams = get("/teams")

        if not teams:
            st.info("Create a team first")
        else:
            team_map = {t[1]: t[0] for t in teams}

            tech = st.text_input("Technician Name", key="tech_name")
            team = st.selectbox("Team", list(team_map.keys()), key="tech_team")

            if st.button("Create Technician"):
                if not tech:
                    st.warning("Technician name required")
                else:
                    post("/technicians", {
                        "name": tech,
                        "team_id": team_map[team]
                    })
                    st.success("Technician added")
                    st.rerun()

    # ---------- Add Equipment ----------
    with st.sidebar.expander("🏭 Add Equipment"):
        teams = get("/teams")
        techs = get("/technicians")

        if not teams or not techs:
            st.info("Create team and technician first")
        else:
            team_map = {t[1]: t[0] for t in teams}
            tech_map = {t[1]: t[0] for t in techs}

            name = st.text_input("Equipment Name", key="eq_name")
            serial = st.text_input("Serial Number", key="eq_serial")
            dept = st.text_input("Department", key="eq_dept")
            owner = st.text_input("Assigned To (Employee)", key="eq_owner")
            location = st.text_input("Location", key="eq_location")

            purchase = st.date_input("Purchase Date", key="eq_purchase")
            warranty = st.date_input("Warranty Expiry", key="eq_warranty")

            team = st.selectbox("Maintenance Team", list(team_map.keys()), key="eq_team")
            tech = st.selectbox("Default Technician", list(tech_map.keys()), key="eq_tech")

            if st.button("Create Equipment"):
                if not all([name, serial, dept, owner, location]):
                    st.warning("All equipment fields are required")
                else:
                    payload = {
                        "name": name,
                        "serial": serial,
                        "department": dept,
                        "employee": owner,
                        "location": location,
                        "purchase_date": str(purchase),
                        "warranty_expiry": str(warranty),
                        "team_id": team_map[team],
                        "default_technician": tech_map[tech]
                    }

                    res = post("/equipment", payload)
                    if res:
                        st.success("Equipment added")
                        st.rerun()

    # ---------- Create Maintenance Request ----------
    with st.sidebar.expander("🛠️ Create Maintenance Request"):
        equipment = get("/equipment")

        if not equipment:
            st.info("Add equipment first")
        else:
            eq_map = {e[1]: e[0] for e in equipment if e[10] == 0}  # ignore scrapped

            subject = st.text_input("Issue / Subject", key="req_subject")
            rtype = st.selectbox(
                "Request Type",
                ["Corrective", "Preventive"],
                key="req_type"
            )
            eq = st.selectbox("Equipment", list(eq_map.keys()), key="req_eq")

            sched_date = None
            if rtype == "Preventive":
                sched_date = st.date_input("Scheduled Date", key="req_date")

            if st.button("Create Request"):
                if not subject:
                    st.warning("Subject is required")
                else:
                    payload = {
                        "subject": subject,
                        "req_type": rtype,
                        "equipment_id": eq_map[eq],
                        "scheduled_date": str(sched_date) if sched_date else None
                    }

                    res = post("/requests", payload)
                    if res:
                        st.success("Request created")
                        st.rerun()
