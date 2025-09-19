# setup_db.py
import sqlite3
import os

DB_NAME = "attendance12.db"

# If DB already exists, remove it (clean slate)
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print(f"Old {DB_NAME} removed ✅")

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Master student table with email + phone
c.execute('''CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                phone_number TEXT,
                parent_email TEXT
            )''')

# Attendance table
c.execute('''CREATE TABLE attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                date TEXT,
                present INTEGER DEFAULT 0,
                FOREIGN KEY(student_id) REFERENCES students(student_id),
                UNIQUE(student_id, date)
            )''')

conn.commit()
conn.close()
print("Fresh database created ✅ with parent_email column")
