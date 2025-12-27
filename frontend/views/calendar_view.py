import streamlit as st
import requests
from datetime import date

API = "http://localhost:8000"

def get(u): return requests.get(API + u).json()

def calendar_view():
    st.subheader("📅 Preventive Maintenance Schedule")

    reqs = get("/requests")
    shown = False

    for r in reqs:
        if r[2] == "Preventive" and r[7]:
            shown = True
            overdue = date.fromisoformat(r[7]) < date.today()

            if overdue:
                st.error(f"{r[1]} — {r[7]} (Overdue)")
            else:
                st.success(f"{r[1]} — {r[7]}")

    if not shown:
        st.info("No preventive maintenance scheduled")

