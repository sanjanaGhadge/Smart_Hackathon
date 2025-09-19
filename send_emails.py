# send_emails.py
import sqlite3
from datetime import date
import os
import time
from email.message import EmailMessage
import smtplib
from deep_translator import GoogleTranslator  # ✅ Used for translation
from dotenv import load_dotenv

load_dotenv()  # loads EMAIL_USER, EMAIL_PASS, SCHOOL_NAME from .env
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SCHOOL_NAME = os.getenv("SCHOOL_NAME", "School")

DB_NAME = "attendance12.db"

# -------------------------
# Function: Get absent students
# -------------------------
def get_absentees(target_date=None):
    if target_date is None:
        target_date = str(date.today())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT s.student_id, s.name, s.parent_email
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        WHERE a.date=? AND a.present=0
    """, (target_date,))
    rows = c.fetchall()
    conn.close()
    return rows, target_date

# -------------------------
# Function: Send Email
# -------------------------
def send_email(to_addr, subject, body):
    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

# -------------------------
# Function: Send absentee emails
# -------------------------
def send_absent_emails(language="pa"):  # ✅ default language Marathi ("mr")
    absentees, target_date = get_absentees()
    if not absentees:
        return f"No absentees for {target_date}"

    sent_count = 0
    skipped_count = 0

    for sid, name, parent_email in absentees:
        if not parent_email or parent_email.endswith("@example.com"):
            skipped_count += 1
            continue

        subject = f"[{SCHOOL_NAME}] Absence notice for {name} — {target_date}"

        # ✅ English message
        english_msg = f"""Dear Parent/Guardian,

This is to inform you that your child {name} (ID: {sid}) was ABSENT on {target_date}.

If you believe this is a mistake, please contact the school office.

Regards,
{SCHOOL_NAME}
"""

        # ✅ Translate message
        try:
            translated_msg = GoogleTranslator(source="en", target=language).translate(english_msg)
        except Exception as e:
            translated_msg = "(Translation failed, showing English only)"

        # ✅ Final body with both English + Translation
        body = f"""{english_msg}

----------------------------------------
[Translated Message]
{translated_msg}
"""

        try:
            send_email(parent_email, subject, body)
            sent_count += 1
        except Exception as e:
            print(f"❌ Failed to send email to {parent_email}: {e}")
            skipped_count += 1

        time.sleep(1)  # polite delay

    return f"Sent emails to {sent_count} absent students for {target_date}, skipped {skipped_count}."


if __name__ == "__main__":
    print(send_absent_emails())
