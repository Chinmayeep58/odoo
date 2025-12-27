import streamlit as st
import requests

API = "http://localhost:8000"

def get(u):
    return requests.get(API + u).json()

def reports_view():
    st.subheader("📊 Maintenance Reports")

    reqs = get("/requests")
    teams = get("/teams")
    equipment = get("/equipment")

    if not reqs:
        st.info("No maintenance requests yet")
        return

    # --- ID → NAME MAPS (based on DEBUG output)
    team_map = {t[0]: t[1] for t in teams}        # id → team name
    eq_map = {e[0]: e[1] for e in equipment}     # id → equipment name

    # ------------------------------
    st.markdown("### 🧑‍🔧 Requests per Team")

    team_count = {}
    for r in reqs:
        team_id = r[5]               # ✅ correct index
        team_name = team_map.get(team_id, "Unknown")
        team_count[team_name] = team_count.get(team_name, 0) + 1

    st.bar_chart(team_count)

    # ------------------------------
    st.markdown("### 🏭 Requests per Equipment")

    eq_count = {}
    for r in reqs:
        eq_id = r[4]                 # ✅ correct index
        eq_name = eq_map.get(eq_id, "Unknown")
        eq_count[eq_name] = eq_count.get(eq_name, 0) + 1

    st.bar_chart(eq_count)

    # ------------------------------
    st.markdown("### 📋 Detailed Request List")

    for r in reqs:
        st.write(
            f"• **{r[1]}** | "
            f"Team: {team_map.get(r[5])} | "
            f"Equipment: {eq_map.get(r[4])} | "
            f"Status: {r[3]}"
        )
