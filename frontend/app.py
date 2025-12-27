import streamlit as st
from views.sidebar import sidebar
from views.kanban import kanban_view
from views.calendar_view import calendar_view
from views.equipment import equipment_view
from views.reports import reports_view

st.set_page_config(
    page_title="GearGuard",
    layout="wide"
)

st.title("🛠️ GearGuard — Maintenance Management System")

sidebar()

tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Kanban Board",
    "📅 Preventive Calendar",
    "🏭 Equipment",
    "📊 Reports"
])

with tab1:
    kanban_view()

with tab2:
    calendar_view()

with tab3:
    equipment_view()

with tab4:
    reports_view()
