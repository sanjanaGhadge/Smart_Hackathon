# insert_students.py
import sqlite3

students = [
    ("S123", "Sanjana", "9876500001", "parent_sanjana@example.com"),
    ("S124", "Amisha", "9876500002", "parent_amisha@example.com"),
    ("S125", "Laxita", "9876500003", "parent_laxita@example.com"),
    ("S126", "Aryan", "9876500004", "parent_aryan@example.com"),
    ("S127", "Chaman", "9876500005", "parent_chaman@example.com"),
    ("S128", "Sneha", "9876500006", "parent_sneha@example.com"),
    ("S129", "Ravi", "9876500007", "parent_ravi@example.com"),
    ("S130", "Pooja", "+919309046542", "sanjanaghadge2023@gmail.com"),
    ("S131", "Srushti","+918767532472", "parent_srushti@example.com"),
    ("S132", "Nisha", "9876500010", "parent_nisha@example.com"),
    
]

conn = sqlite3.connect("attendance12.db")   # ✅ using your new DB name
c = conn.cursor()

c.executemany(
    "INSERT OR IGNORE INTO students (student_id, name, phone_number, parent_email) VALUES (?, ?, ?, ?)",
    students
)

conn.commit()
conn.close()
print("✅ 10 students added to master table in attendance12.db")
