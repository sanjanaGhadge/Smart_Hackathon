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
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create and activate virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On Linux/Mac
   venv\Scripts\activate        # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠️ Usage

1. **Step 1: Initialize Database**
   ```bash
   python setup_db.py
   ```

2. **Step 2: Insert Student Records**
   ```bash
   python insert_students.py
   ```

3. **Step 3: Start Backend Server**
   ```bash
   python scanning.py
   ```

4. **Step 4: Run Frontend Application**
   ```bash
   python app2.py
   ```

---

## 📌 Notes

- Ensure that the database is created using `setup_db.py` before running other scripts.  
- `insert_students.py` should be run only once after initial setup (or whenever you want to add bulk student data).  
- Keep the **server (`scanning.py`) running** while using the frontend (`app2.py`).  

---

## 👩‍💻 Authors
- Team <Your Team Name> – Smart India Hackathon  
