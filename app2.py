from flask import Flask, render_template, request, send_file
import sqlite3
from datetime import date
import csv
import io
from flask import jsonify
from send_emails import send_absent_emails
from send_sms import send_absent_sms  

app = Flask(__name__)

DB_NAME = "attendance12.db"

def get_attendance(filter_status=None, filter_date=None):
    if filter_date is None:
        filter_date = str(date.today())
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    query = """
        SELECT s.student_id, s.name, s.parent_email,
               COALESCE(a.present, 0) AS present
        FROM students s
        LEFT JOIN attendance a
        ON s.student_id = a.student_id AND a.date = ?
        ORDER BY s.student_id
    """
    
    c.execute(query, (filter_date,))
    rows = c.fetchall()
    conn.close()
    
    if filter_status == "P":
        rows = [r for r in rows if r[3] == 1]
    elif filter_status == "A":
        rows = [r for r in rows if r[3] == 0]
    
    return rows

@app.route("/", methods=["GET"])
def index():
    filter_status = request.args.get("filter")
    filter_date = request.args.get("date")
    records = get_attendance(filter_status, filter_date)
    return render_template("index1.html", records=records, filter_status=filter_status, filter_date=filter_date)

@app.route("/download_csv")
def download_csv():
    filter_status = request.args.get("filter")
    filter_date = request.args.get("date")
    records = get_attendance(filter_status, filter_date)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Name", "Email", "Status"])
    for student_id, name, email, present in records:
        writer.writerow([student_id, name, email, 'P' if present else 'A'])
    
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name=f"attendance_{filter_date or date.today()}.csv")

@app.route("/send_emails_ajax")
def send_emails_ajax():
    try:
        result = send_absent_emails()
    except Exception as e:
        result = f"Error sending emails: {str(e)}"
    return jsonify({"message": result})

@app.route("/send_sms_ajax")
def send_sms_ajax():
    try:
        result = send_absent_sms()
    except Exception as e:
        result = f"Error sending SMS: {str(e)}"
    return jsonify({"message": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
