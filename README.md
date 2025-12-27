# 🛠️ GearGuard — Smart Maintenance Management System

GearGuard is a lightweight maintenance management platform inspired by Odoo — built to help teams **track equipment, assign technicians, manage repair requests, and schedule preventive maintenance** in one clean dashboard.

---

## ⭐ Why GearGuard?

Most companies still track maintenance using WhatsApp, Excel, or paper logs — which leads to:

❌ Missed preventive services  
❌ No ownership or accountability  
❌ Zero visibility on machine health  
❌ Reactive breakdown fixes instead of planning  

**GearGuard fixes this by bringing structure + visibility without complexity.**

---

## 🚀 What GearGuard Does

### ✔ Track Equipment
Store key details like owner, department, warranty & assigned maintenance team.

### ✔ Create Maintenance Requests
Types supported:
- 🛠️ **Corrective** — breakdown repair
- 🔄 **Preventive** — scheduled servicing

### ✔ Kanban Workflow
Stages:
➡️ New → In Progress → Repaired → Scrap

### ✔ Automatic Assignment
Requests auto-link to:
🔧 Correct maintenance team  
👨‍🔧 Default technician  

### ✔ Preventive Calendar
Never miss upcoming service jobs.

### ✔ Scrap Logic
If a request reaches **Scrap**, the system marks the equipment as unusable.

---

## 🧑‍💻 How It’s Built 

- **Frontend:** Streamlit (clean UI, no setup needed)
- **Backend:** FastAPI
- **Database:** SQLite (auto-created)

Lightweight. Portable. Hackathon-ready.

---

## ▶️ How to Run (Simple)

### 1️⃣ Start Backend
```

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

```

Backend runs at:
```

(http://localhost:8000)

```

### 2️⃣ Start Frontend
```

cd frontend
pip install -r requirements.txt
streamlit run app.py

```

UI opens at:
```

(http://localhost:8501)

```

---

## 🔍 Example Use-Case

1️⃣ Create a **Maintenance Team**  
2️⃣ Assign **Technicians**  
3️⃣ Register **Equipment**  
4️⃣ Log a **Repair Request**  
5️⃣ Track progress on **Kanban Board**  
6️⃣ Schedule preventive checks on **Calendar**

---

## 💡 What Makes GearGuard Special?

✨ Simple — teams actually USE it  
✨ Smart defaults — auto assignment  
✨ Preventive first — reduce breakdowns  
✨ Transparent — clear accountability  
✨ Deploy anywhere — runs on SQLite  

---

## 📌 Future Enhancements

🧠 AI-based failure predictions  
📊 Analytics dashboard  
📧 Alerts & reminders  
🔐 Role-based access  

---

## 👥 Built For

Manufacturing • Facilities • IT • Admin • Campus Ops • Labs

---
