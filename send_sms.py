# send_sms.py
import sqlite3
from datetime import date
from twilio.rest import Client
from deep_translator import GoogleTranslator  # ✅ added translator
from dotenv import load_dotenv
import os

load_dotenv()

ACCOUNT_SID =os.getenv("ACCOUNT_SID")
AUTH_TOKEN =os.getenv("AUTH_TOKEN")
TWILIO_PHONE =os.getenv("TWILIO_PHONE")

DB_NAME = "attendance12.db"

# Toggle test mode: True = simulate, False = actually send SMS
TEST_MODE = True  

# Change this to "pa" for Punjabi, "mr" for Marathi, "hi" for Hindi, etc.
TARGET_LANG = "mr"  

def send_absent_sms():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    today = str(date.today())
    # Fetch absent students with phone numbers
    c.execute('''
        SELECT s.name, s.phone_number
        FROM students s
        LEFT JOIN attendance a
        ON s.student_id = a.student_id AND a.date = ?
        WHERE COALESCE(a.present, 0) = 0
    ''', (today,))
    
    absentees = c.fetchall()
    conn.close()
    
    if not absentees:
        return "No absent students to notify via SMS ✅"

    # Initialize Twilio client only if not in test mode
    if not TEST_MODE:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

    count = 0
    for name, phone in absentees:
        if not phone:
            continue
        
        english_msg = f"Hello, {name} is absent today ({today})."
        # Translate to regional language
        translated_msg = GoogleTranslator(source="en", target=TARGET_LANG).translate(english_msg)

        # Final message = English + Translation
        msg_text = english_msg + "\n" + translated_msg

        if TEST_MODE:
            print(f"[TEST MODE] Would send SMS to {phone}: {msg_text}")
        else:
            try:
                message = client.messages.create(
                    body=msg_text,
                    from_=TWILIO_PHONE,
                    to=phone  # Must be verified in trial
                )
                print(f"SMS sent to {name} ({phone}), SID: {message.sid}")
            except Exception as e:
                print(f"Failed to send SMS to {phone}: {e}")
        count += 1

    return f"Processed {count} absent students (SMS {'simulated' if TEST_MODE else 'sent'}) 📱"
