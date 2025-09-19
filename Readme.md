# 📚 Smart Attendance System (SIH Project)

This project is a **Smart Attendance System** developed for SIH (Smart India Hackathon).  
It uses Python-based scripts for **database setup, data insertion, server operations, and frontend interaction**.

---

## 🚀 Project Structure

- **`setup_db.py`** → Initializes and creates the database schema. Must be run first.  
- **`insert_students.py`** → Inserts initial student data into the database. Run only after `setup_db.py`.  
- **`scanning.py`** → Acts as the server script to handle backend operations (e.g., scanning, processing requests).  
- **`app2.py`** → Frontend application that interacts with the server and database.  

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanjanaGhadge/Smart_Hackathon.git
   cd Smart_Hackathon
Create and activate virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate        # On Windows
Install dependencies

pip install -r requirements.txt
🛠️ Usage
Step 1: Initialize Database

python setup_db.py
Step 2: Insert Student Records

python insert_students.py
Step 3: Start Backend Server

python scanning.py
Step 4: Run Frontend Application

python app2.py
📌 Notes
Ensure that the database is created using setup_db.py before running other scripts.

insert_students.py should be run only once after initial setup (or whenever you want to add bulk student data).

Keep the server (scanning.py) running while using the frontend (app2.py).