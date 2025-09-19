import cv2
import sqlite3
from datetime import date

DB_NAME = "attendance12.db"
today = str(date.today())

# Connect once
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

# --- STEP 1: Ensure today's attendance exists for all students ---
c.execute("SELECT COUNT(*) FROM attendance WHERE date=?", (today,))
count = c.fetchone()[0]

if count == 0:
    print(f"ℹ️ Initializing attendance for {today}...")
    c.execute("SELECT student_id FROM students")
    students = c.fetchall()
    for (student_id,) in students:
        c.execute(
            "INSERT INTO attendance (student_id, date, present) VALUES (?, ?, ?)",
            (student_id, today, 0),  # default absent
        )
    conn.commit()
    print("✅ Attendance initialized for all students.")

# --- QR Scanning Logic ---
detector = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)

last_detected_id = None  # To avoid spamming when QR stays in camera

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera not available. Exiting...")
        break

    try:
        data, bbox, _ = detector.detectAndDecode(frame)
    except cv2.error:
        data, bbox = None, None  # Skip invalid detection

    if bbox is not None and data:
        student_id = data.split("|")[0].strip()

        if student_id != last_detected_id:  # Only react when QR changes
            last_detected_id = student_id

            # Check today's record (guaranteed to exist now)
            c.execute(
                "SELECT present FROM attendance WHERE student_id=? AND date=?",
                (student_id, today),
            )
            row = c.fetchone()

            if row:
                if row[0] == 1:
                    print(f"ℹ️ {student_id} already marked present for {today}.")
                else:
                    # Mark as present
                    c.execute(
                        "UPDATE attendance SET present=1 WHERE student_id=? AND date=?",
                        (student_id, today),
                    )
                    conn.commit()
                    print(f"✅ {student_id} marked present for {today}.")
            else:
                # Should not happen anymore since we pre-initialized
                print(f"⚠️ {student_id} not found in DB for {today}.")
    else:
        last_detected_id = None  # Reset when no QR visible

    # Show camera window
    cv2.imshow("QR Scanner - Press 'q' to quit", frame)

    # Keep running until you press q
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("👋 Exiting scanner...")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
conn.close()
