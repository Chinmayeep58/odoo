import streamlit as st
import requests

API = "http://localhost:8000"

def get(u): return requests.get(API + u).json()
def put(u, p): return requests.put(API + u, json=p).json()

def kanban_view():
    st.subheader("📌 Maintenance Kanban")

    states = ["New", "In Progress", "Repaired", "Scrap"]
    reqs = get("/requests")

    if not reqs:
        st.info("No maintenance requests found")
        return

    cols = st.columns(4)

    for i, state in enumerate(states):
        with cols[i]:
            st.markdown(f"### {state}")

            for r in reqs:
                if r[3] == state:  # ✅ correct index
                    with st.container(border=True):
                        st.write(f"**{r[1]}**")
                        st.caption(f"Type: {r[2]}")

                        if state != "Scrap":
                            if st.button("→ Next", key=f"{r[0]}{state}"):
                                put(f"/requests/{r[0]}", {
                                    "state": states[i + 1]
                                })
                                st.rerun()

