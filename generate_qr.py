# generate_qr.py
import qrcode

students = [
    {"id": "S123", "name": "Sanjana"},
    {"id": "S124", "name": "Amisha"},
    {"id": "S125", "name": "Laxita"},
    {"id": "S126", "name": "Aryan"},     # NEW
    {"id": "S127", "name": "Chaman"},     # NEW
    {"id": "S128", "name": "Sneha"}, 
]

for student in students:
    payload = f"{student['id']}|{student['name']}"
    img = qrcode.make(payload)
    img.save(f"{student['id']}.png")
    print(f"QR saved for {student['name']}")
