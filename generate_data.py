"""
Data Generator for Hostel Booking and Management System
Generates:
- 4 Blocks (A, B, C, D)
- 6 Floors per block (1 to 6)
- 10 Rooms per floor (101-110, 201-210, etc.) = 60 rooms/block = 240 rooms total
- 5 Beds per room = 1,200 total student capacity
- Mix of AC/Non-AC, Attached/Common bathroom, realistic pricing, occupants, and statuses.
"""

import json
import sqlite3
import os
import random
from datetime import datetime, timedelta

PROJECT_DIR = r"C:\Users\Ameen\.gemini\antigravity\scratch\hostel-booking-management-system"
DB_PATH = os.path.join(PROJECT_DIR, "hostel.db")
SEED_JSON_PATH = os.path.join(PROJECT_DIR, "initial_data.json")

BLOCK_NAMES = ["Block A", "Block B", "Block C", "Block D"]
BLOCK_METADATA = {
    "Block A": {"tag": "Boys Block - Alpha", "gender": "Male", "wings": "North Wing", "incharge": "Mr. Suresh Nair (9845112233)"},
    "Block B": {"tag": "Boys Block - Beta", "gender": "Male", "wings": "East Wing", "incharge": "Mr. Ramesh Joshi (9845112244)"},
    "Block C": {"tag": "Girls Block - Gamma", "gender": "Female", "wings": "South Wing", "incharge": "Dr. Sunita Rao (9845112255)"},
    "Block D": {"tag": "Girls Block - Delta", "gender": "Female", "wings": "West Wing", "incharge": "Mrs. Anita Deshmukh (9845112266)"}
}

ROOM_IMAGES = [
    "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1540518614846-7ede433c4550?auto=format&fit=crop&w=800&q=80",
    "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80"
]

def generate_rooms():
    rooms = []
    # Seed reproducible random
    random.seed(42)

    for b_idx, block in enumerate(BLOCK_NAMES):
        for floor in range(1, 7):
            for r in range(1, 11):
                room_num = floor * 100 + r
                room_id = f"{block.replace(' ', '')}-{room_num}"
                
                # Assign room attributes
                # Floor 1-3 mostly Non-AC with some AC, Floor 4-6 mostly AC
                is_ac = (floor >= 4) or (r % 2 == 0)
                room_type = "AC" if is_ac else "Non-AC"
                
                # Rooms 1 to 6 have Attached bathroom, 7 to 10 Common
                has_attached = (r <= 6)
                bath_type = "Attached" if has_attached else "Common"
                
                # Pricing
                base_rent = 8500 if is_ac else 6000
                if has_attached:
                    base_rent += 1000
                deposit = 10000

                # Fixed status / occupancy for initial realism
                # 2 rooms in total under maintenance
                if room_id in ["BlockA-105", "BlockB-307", "BlockC-502"]:
                    status = "Maintenance"
                    occupied = 0
                else:
                    # Distribute realistic occupancy: some 0, some 1-4, some 5
                    dice = (b_idx * 60 + (floor-1) * 10 + r) % 10
                    if dice == 0:
                        occupied = 0  # Available
                        status = "Available"
                    elif dice in [1, 2, 3]:
                        occupied = 5  # Fully occupied
                        status = "Fully Occupied"
                    else:
                        occupied = (dice % 4) + 1  # 1 to 4 occupied
                        status = "Partially Occupied"

                facilities = [
                    "High-Speed Wi-Fi",
                    "Study Desk & Chair",
                    "Individual Locker Wardrobe",
                    "Power Backup"
                ]
                if is_ac:
                    facilities.append("Split Air Conditioner")
                if has_attached:
                    facilities.append("Attached Western Bath")
                    facilities.append("24/7 Geyser Hot Water")
                else:
                    facilities.append("Spacious Common Bath")

                img = ROOM_IMAGES[(floor + r) % len(ROOM_IMAGES)]

                rooms.append({
                    "id": room_id,
                    "block": block,
                    "floor": floor,
                    "room_number": room_num,
                    "capacity": 5,
                    "occupied_beds": occupied,
                    "available_beds": 5 - occupied if status != "Maintenance" else 0,
                    "room_type": room_type,
                    "bathroom_type": bath_type,
                    "rent": base_rent,
                    "deposit": deposit,
                    "status": status,
                    "facilities": facilities,
                    "image": img,
                    "description": f"Spacious {room_type} 5-sharing room in {block}, Floor {floor}. Features {bath_type.lower()} bathroom, individual study stations, and premium natural ventilation."
                })
    return rooms

def generate_sample_students(rooms):
    students = [
        {
            "id": "STU-001",
            "name": "Rahul Sharma",
            "email": "rahul@student.com",
            "password": "password123",
            "role": "student",
            "mobile": "9876543210",
            "gender": "Male",
            "college": "National Institute of Technology",
            "department": "Computer Science & Engineering",
            "year": "3rd Year",
            "parent_name": "Satish Sharma",
            "parent_contact": "9876543299",
            "address": "42, Shanti Nagar, Jaipur, Rajasthan",
            "block": "Block A",
            "floor": 2,
            "room_id": "BlockA-201",
            "room_number": 201,
            "bed_number": 2,
            "room_type": "AC",
            "bathroom_type": "Attached",
            "monthly_rent": 9500,
            "deposit_paid": 10000,
            "checkin_date": "2026-08-01",
            "status": "Active",
            "vacating_date": None,
            "vacating_reason": None,
            "id_proof": "aadhaar_verified.pdf",
            "profile_photo": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=300&q=80"
        },
        {
            "id": "STU-002",
            "name": "Priya Patel",
            "email": "priya@student.com",
            "password": "password123",
            "role": "student",
            "mobile": "9876543211",
            "gender": "Female",
            "college": "State Technological University",
            "department": "Electronics & Communication",
            "year": "2nd Year",
            "parent_name": "Mahesh Patel",
            "parent_contact": "9876543298",
            "address": "15, Navrangpura, Ahmedabad, Gujarat",
            "block": "Block C",
            "floor": 1,
            "room_id": "BlockC-102",
            "room_number": 102,
            "bed_number": 1,
            "room_type": "Non-AC",
            "bathroom_type": "Attached",
            "monthly_rent": 7000,
            "deposit_paid": 10000,
            "checkin_date": "2026-08-15",
            "status": "Active",
            "vacating_date": None,
            "vacating_reason": None,
            "id_proof": "college_id_card.pdf",
            "profile_photo": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80"
        },
        {
            "id": "STU-003",
            "name": "Amit Kumar",
            "email": "amit@student.com",
            "password": "password123",
            "role": "student",
            "mobile": "9876543212",
            "gender": "Male",
            "college": "Delhi Technological University",
            "department": "Mechanical Engineering",
            "year": "4th Year",
            "parent_name": "Rakesh Kumar",
            "parent_contact": "9876543297",
            "address": "B-88, Rohini Sector 7, New Delhi",
            "block": "Block B",
            "floor": 4,
            "room_id": "BlockB-403",
            "room_number": 403,
            "bed_number": 4,
            "room_type": "AC",
            "bathroom_type": "Attached",
            "monthly_rent": 9500,
            "deposit_paid": 10000,
            "checkin_date": "2026-07-20",
            "status": "Active",
            "vacating_date": None,
            "vacating_reason": None,
            "id_proof": "voter_card.pdf",
            "profile_photo": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=300&q=80"
        },
        {
            "id": "STU-004",
            "name": "Sneha Reddy",
            "email": "sneha@student.com",
            "password": "password123",
            "role": "student",
            "mobile": "9876543213",
            "gender": "Female",
            "college": "Hyderabad City College of Science",
            "department": "Data Science",
            "year": "4th Year",
            "parent_name": "Venkatesh Reddy",
            "parent_contact": "9876543296",
            "address": "Flat 302, Banjara Hills, Hyderabad, Telangana",
            "block": "Block D",
            "floor": 3,
            "room_id": "BlockD-304",
            "room_number": 304,
            "bed_number": 3,
            "room_type": "AC",
            "bathroom_type": "Common",
            "monthly_rent": 8000,
            "deposit_paid": 10000,
            "checkin_date": "2026-01-10",
            "status": "Vacating Requested",
            "vacating_date": "2026-11-30",
            "vacating_reason": "Final semester completed. Relocating for corporate internship.",
            "id_proof": "passport_scan.pdf",
            "profile_photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80"
        },
        {
            "id": "STU-005",
            "name": "Vikram Singh",
            "email": "vikram@student.com",
            "password": "password123",
            "role": "student",
            "mobile": "9876543214",
            "gender": "Male",
            "college": "Institute of Engineering & Tech",
            "department": "Civil Engineering",
            "year": "1st Year",
            "parent_name": "Dhirendra Singh",
            "parent_contact": "9876543295",
            "address": "Sector 14, Chandigarh, Punjab",
            "block": "Block A",
            "floor": 1,
            "room_id": None,
            "room_number": None,
            "bed_number": None,
            "room_type": "Non-AC",
            "bathroom_type": "Common",
            "monthly_rent": 6000,
            "deposit_paid": 0,
            "checkin_date": "2026-12-01",
            "status": "Pending Approval",
            "vacating_date": None,
            "vacating_reason": None,
            "id_proof": "student_admission_letter.pdf",
            "profile_photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=300&q=80"
        }
    ]

    # Admin user
    admins = [
        {
            "id": "ADM-001",
            "name": "Dr. Rajesh Verma",
            "email": "admin@hostel.com",
            "password": "admin123",
            "role": "admin",
            "mobile": "9811223344",
            "gender": "Male",
            "college": "Hostel Central Administration",
            "department": "Chief Warden Office",
            "year": "Staff",
            "parent_name": "N/A",
            "parent_contact": "011-28776655",
            "address": "Staff Quarters #4, Hostel Campus",
            "status": "Active",
            "profile_photo": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=300&q=80"
        }
    ]
    return students, admins

def generate_sample_complaints():
    return [
        {
            "id": "CMP-1001",
            "student_id": "STU-001",
            "student_name": "Rahul Sharma",
            "room_id": "BlockA-201",
            "category": "Wi-Fi problems",
            "title": "Intermittent Wi-Fi signal in room A-201",
            "description": "The 5GHz Wi-Fi signal keeps dropping frequently every evening between 7 PM and 10 PM. Speed tests show under 2 Mbps during peak study hours.",
            "photo": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?auto=format&fit=crop&w=400&q=80",
            "status": "In Progress",
            "priority": "High",
            "admin_remarks": "IT team scheduled a dual-band access point installation on Floor 2 tomorrow morning at 10:00 AM.",
            "created_at": "2026-11-10 14:30"
        },
        {
            "id": "CMP-1002",
            "student_id": "STU-002",
            "student_name": "Priya Patel",
            "room_id": "BlockC-102",
            "category": "Bathroom cleaning",
            "title": "Attached bathroom drainage pipe slow flow",
            "description": "Water drains very slowly after shower in the attached bathroom. Requires plumbing unblocking check.",
            "photo": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=400&q=80",
            "status": "Resolved",
            "priority": "Medium",
            "admin_remarks": "Housekeeping and plumbing technician cleared the hair trap and flushed pipe on 2026-11-12.",
            "created_at": "2026-11-11 09:15"
        },
        {
            "id": "CMP-1003",
            "student_id": "STU-003",
            "student_name": "Amit Kumar",
            "room_id": "BlockB-403",
            "category": "Electricity problems",
            "title": "Study desk power outlet loose connection",
            "description": "The 3-pin power socket near bed #4 sparks slightly when laptop charger is plugged in. Needs socket plate replacement.",
            "photo": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=400&q=80",
            "status": "Pending",
            "priority": "High",
            "admin_remarks": "Assigned to Campus Electrician Mr. Mohan for inspection.",
            "created_at": "2026-11-12 18:40"
        },
        {
            "id": "CMP-1004",
            "student_id": "STU-004",
            "student_name": "Sneha Reddy",
            "room_id": "BlockD-304",
            "category": "Water problems",
            "title": "Low water pressure in 3rd floor washrooms",
            "description": "Between 6:30 AM and 8:00 AM, common washroom taps have low pressure due to pump scheduling.",
            "photo": None,
            "status": "In Progress",
            "priority": "Medium",
            "admin_remarks": "Facility team is adjusting overhead booster pump timers.",
            "created_at": "2026-11-13 08:20"
        }
    ]

def generate_sample_payments():
    return [
        {
            "id": "PAY-882101",
            "student_id": "STU-001",
            "student_name": "Rahul Sharma",
            "room_id": "BlockA-201",
            "month": "November 2026",
            "amount": 9500,
            "deposit": 10000,
            "type": "Monthly Rent (AC Attached)",
            "payment_method": "UPI - PhonePe",
            "transaction_ref": "UPI20261102987112",
            "status": "Paid",
            "payment_date": "2026-11-02 11:20:00",
            "invoice_no": "INV-2026-11-001"
        },
        {
            "id": "PAY-882102",
            "student_id": "STU-002",
            "student_name": "Priya Patel",
            "room_id": "BlockC-102",
            "month": "November 2026",
            "amount": 7000,
            "deposit": 10000,
            "type": "Monthly Rent (Non-AC Attached)",
            "payment_method": "Credit Card (HDFC)",
            "transaction_ref": "CC9845210984",
            "status": "Paid",
            "payment_date": "2026-11-03 14:15:30",
            "invoice_no": "INV-2026-11-002"
        },
        {
            "id": "PAY-882103",
            "student_id": "STU-003",
            "student_name": "Amit Kumar",
            "room_id": "BlockB-403",
            "month": "November 2026",
            "amount": 9500,
            "deposit": 10000,
            "type": "Monthly Rent (AC Attached)",
            "payment_method": "Net Banking (SBI)",
            "transaction_ref": "NETBK44332211",
            "status": "Paid",
            "payment_date": "2026-11-05 16:45:10",
            "invoice_no": "INV-2026-11-003"
        },
        {
            "id": "PAY-882104",
            "student_id": "STU-004",
            "student_name": "Sneha Reddy",
            "room_id": "BlockD-304",
            "month": "November 2026",
            "amount": 8000,
            "deposit": 10000,
            "type": "Monthly Rent (AC Common)",
            "payment_method": "Pending",
            "transaction_ref": None,
            "status": "Pending",
            "payment_date": None,
            "invoice_no": "INV-2026-11-004"
        }
    ]

def generate_sample_notices():
    return [
        {
            "id": "NOT-01",
            "title": "Annual Hostel Sports & Badminton Tournament",
            "category": "Event",
            "priority": "Normal",
            "author": "Chief Warden Office",
            "content": "Registrations are now open for the Inter-Block Table Tennis and Badminton Tournament starting this Saturday, 21st November in the indoor sports complex. Attractive trophies and cash prizes for winning blocks!",
            "date": "2026-11-13"
        },
        {
            "id": "NOT-02",
            "title": "Scheduled Solar Geyser System Maintenance",
            "category": "Maintenance",
            "priority": "High",
            "author": "Facility Maintenance Dept",
            "content": "Routine cleaning and descaling of solar hot water collector panels will take place on Sunday, 15th November between 11:00 AM and 3:00 PM. Hot water will resume normally via electrical backup by 4:00 PM.",
            "date": "2026-11-12"
        },
        {
            "id": "NOT-03",
            "title": "Dining Hall Special Festive Menu Feedback",
            "category": "Mess Committee",
            "priority": "Normal",
            "author": "Student Mess Committee",
            "content": "The student mess committee invites all residents to submit their menu suggestions for the upcoming winter feast. Please submit your recommendations through the complaint/feedback portal by Wednesday.",
            "date": "2026-11-10"
        },
        {
            "id": "NOT-04",
            "title": "Hostel Gate Timings & Safety Guidelines Reminder",
            "category": "Regulation",
            "priority": "Urgent",
            "author": "Chief Security Officer",
            "content": "All students are reminded that main hostel entry gates close strictly at 10:30 PM. Late entry requires prior approval on the student dashboard or permission letter from department HOD.",
            "date": "2026-11-08"
        }
    ]

def init_all():
    rooms = generate_rooms()
    students, admins = generate_sample_students(rooms)
    complaints = generate_sample_complaints()
    payments = generate_sample_payments()
    notices = generate_sample_notices()

    full_data = {
        "metadata": {
            "title": "Hostel Booking and Management System",
            "version": "2.0.0",
            "total_blocks": 4,
            "floors_per_block": 6,
            "rooms_per_floor": 10,
            "total_rooms": 240,
            "bed_capacity_per_room": 5,
            "total_student_capacity": 1200
        },
        "blocks": BLOCK_NAMES,
        "block_details": BLOCK_METADATA,
        "rooms": rooms,
        "students": students,
        "admins": admins,
        "complaints": complaints,
        "payments": payments,
        "notices": notices
    }

    # Save to JSON
    with open(SEED_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2)
    print(f"Generated initial_data.json ({len(rooms)} rooms, {len(students)} students)")

    # Init SQLite database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS rooms")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS complaints")
    cur.execute("DROP TABLE IF EXISTS payments")
    cur.execute("DROP TABLE IF EXISTS notices")

    cur.execute("""
    CREATE TABLE rooms (
        id TEXT PRIMARY KEY,
        block TEXT NOT NULL,
        floor INTEGER NOT NULL,
        room_number INTEGER NOT NULL,
        capacity INTEGER DEFAULT 5,
        occupied_beds INTEGER DEFAULT 0,
        available_beds INTEGER DEFAULT 5,
        room_type TEXT NOT NULL,
        bathroom_type TEXT NOT NULL,
        rent INTEGER NOT NULL,
        deposit INTEGER NOT NULL,
        status TEXT NOT NULL,
        facilities TEXT,
        image TEXT,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        mobile TEXT,
        gender TEXT,
        college TEXT,
        department TEXT,
        year TEXT,
        parent_name TEXT,
        parent_contact TEXT,
        address TEXT,
        block TEXT,
        floor INTEGER,
        room_id TEXT,
        room_number INTEGER,
        bed_number INTEGER,
        room_type TEXT,
        bathroom_type TEXT,
        monthly_rent INTEGER,
        deposit_paid INTEGER,
        checkin_date TEXT,
        status TEXT,
        vacating_date TEXT,
        vacating_reason TEXT,
        id_proof TEXT,
        profile_photo TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE complaints (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        student_name TEXT,
        room_id TEXT,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        photo TEXT,
        status TEXT DEFAULT 'Pending',
        priority TEXT DEFAULT 'Medium',
        admin_remarks TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE payments (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        student_name TEXT,
        room_id TEXT,
        month TEXT,
        amount INTEGER NOT NULL,
        deposit INTEGER,
        type TEXT,
        payment_method TEXT,
        transaction_ref TEXT,
        status TEXT,
        payment_date TEXT,
        invoice_no TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE notices (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT,
        priority TEXT,
        author TEXT,
        content TEXT NOT NULL,
        date TEXT
    )
    """)

    # Populate rooms
    for r in rooms:
        cur.execute("""
        INSERT INTO rooms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["id"], r["block"], r["floor"], r["room_number"], r["capacity"],
            r["occupied_beds"], r["available_beds"], r["room_type"], r["bathroom_type"],
            r["rent"], r["deposit"], r["status"], json.dumps(r["facilities"]),
            r["image"], r["description"]
        ))

    # Populate users (students + admins)
    for u in students:
        cur.execute("""
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            u["id"], u["name"], u["email"], u["password"], u["role"], u["mobile"],
            u["gender"], u["college"], u["department"], u["year"], u["parent_name"],
            u["parent_contact"], u["address"], u["block"], u["floor"], u["room_id"],
            u["room_number"], u["bed_number"], u["room_type"], u["bathroom_type"],
            u["monthly_rent"], u["deposit_paid"], u["checkin_date"], u["status"],
            u["vacating_date"], u["vacating_reason"], u["id_proof"], u["profile_photo"]
        ))

    for a in admins:
        cur.execute("""
        INSERT INTO users (id, name, email, password, role, mobile, gender, college, department, year, parent_name, parent_contact, address, status, profile_photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            a["id"], a["name"], a["email"], a["password"], a["role"], a["mobile"],
            a["gender"], a["college"], a["department"], a["year"], a["parent_name"],
            a["parent_contact"], a["address"], a["status"], a["profile_photo"]
        ))

    # Populate complaints
    for c in complaints:
        cur.execute("""
        INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["id"], c["student_id"], c["student_name"], c["room_id"],
            c["category"], c["title"], c["description"], c["photo"],
            c["status"], c["priority"], c["admin_remarks"], c["created_at"]
        ))

    # Populate payments
    for p in payments:
        cur.execute("""
        INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["student_id"], p["student_name"], p["room_id"],
            p["month"], p["amount"], p["deposit"], p["type"],
            p["payment_method"], p["transaction_ref"], p["status"],
            p["payment_date"], p["invoice_no"]
        ))

    # Populate notices
    for n in notices:
        cur.execute("""
        INSERT INTO notices VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            n["id"], n["title"], n["category"], n["priority"],
            n["author"], n["content"], n["date"]
        ))

    conn.commit()
    conn.close()
    print("Database hostel.db initialized successfully!")

if __name__ == "__main__":
    init_all()
