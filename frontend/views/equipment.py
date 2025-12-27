import streamlit as st
import requests

API = "http://localhost:8000"

def get(u): return requests.get(API + u).json()

def equipment_view():
    st.subheader("🏭 Equipment Registry")
    equipment = get("/equipment")
    requests_data = get("/requests")

    if not equipment:
        st.info("No equipment added")
        return

    for e in equipment:
        with st.container(border=True):
            st.write(f"### {e[1]} ({e[2]})")
            st.caption(f"Dept: {e[3]} | Owner: {e[4]}")
            st.caption(f"Location: {e[5]}")

            open_count = len([
                r for r in requests_data
                if r[4] == e[0] and r[3] not in ("Repaired", "Scrap")
            ])

            st.write(f"🛠️ Open Requests: **{open_count}**")

            with st.expander("View Maintenance Requests"):
                for r in requests_data:
                    if r[4] == e[0]:
                        st.write(f"- {r[1]} ({r[3]})")

