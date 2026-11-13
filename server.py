"""
Hostel Booking and Management System - Python Backend Server
Serves static frontend files and provides a complete RESTful JSON API using SQLite.
No external dependencies required (uses standard library http.server, sqlite3, json).
"""

import http.server
import socketserver
import urllib.parse
import json
import sqlite3
import os
import sys
import mimetypes
import uuid
import random
from datetime import datetime

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "hostel.db")

# Store in-memory OTPs for verification
OTP_STORE = {}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def recalculate_room_status(cur, room_id):
    """Update room availability and status based on occupied beds."""
    cur.execute("SELECT capacity, occupied_beds, status FROM rooms WHERE id = ?", (room_id,))
    row = cur.fetchone()
    if not row:
        return
    cap = row["capacity"] or 5
    occ = row["occupied_beds"] or 0
    curr_status = row["status"]
    
    if curr_status == "Maintenance":
        avail = 0
    else:
        avail = max(0, cap - occ)
        if occ >= cap:
            curr_status = "Fully Occupied"
        elif occ == 0:
            curr_status = "Available"
        else:
            curr_status = "Partially Occupied"
            
    cur.execute("""
    UPDATE rooms 
    SET occupied_beds = ?, available_beds = ?, status = ?
    WHERE id = ?
    """, (occ, avail, curr_status, room_id))

class HostelRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for local dev / Live Server compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status_code=200):
        response_bytes = json.dumps(data, default=str).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def parse_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                return json.loads(body)
            except Exception:
                return {}
        return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API routing
        if path.startswith('/api/'):
            self.handle_api_get(path, query)
        else:
            # Default to index.html if root requested
            if path == '/' or path == '':
                self.path = '/index.html'
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        data = self.parse_body()
        if path.startswith('/api/'):
            self.handle_api_post(path, data)
        else:
            self.send_error(404, "Not Found")

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        data = self.parse_body()
        if path.startswith('/api/'):
            self.handle_api_put(path, data)
        else:
            self.send_error(404, "Not Found")

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith('/api/'):
            self.handle_api_delete(path)
        else:
            self.send_error(404, "Not Found")

    # API HANDLERS
    def handle_api_get(self, path, query):
        conn = get_db()
        cur = conn.cursor()

        try:
            if path == '/api/stats':
                # Overall hostel statistics
                cur.execute("SELECT COUNT(*) FROM rooms")
                total_rooms = cur.fetchone()[0]

                cur.execute("SELECT SUM(capacity), SUM(occupied_beds), SUM(available_beds) FROM rooms")
                cap_row = cur.fetchone()
                total_cap = cap_row[0] or 1200
                total_occupied = cap_row[1] or 0
                total_avail = cap_row[2] or 0

                cur.execute("SELECT COUNT(*) FROM rooms WHERE room_type = 'AC'")
                ac_rooms = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM rooms WHERE room_type = 'Non-AC'")
                non_ac_rooms = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'Active'")
                active_students = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'Vacated'")
                vacated_students = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'Pending Approval'")
                pending_bookings = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND status = 'Vacating Requested'")
                vacating_requests = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM complaints WHERE status != 'Resolved'")
                pending_complaints = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'")
                resolved_complaints = cur.fetchone()[0]

                cur.execute("SELECT SUM(amount) FROM payments WHERE status = 'Paid'")
                total_revenue = cur.fetchone()[0] or 0

                stats = {
                    "total_blocks": 4,
                    "total_floors": 24,
                    "total_rooms": total_rooms,
                    "total_capacity": total_cap,
                    "occupied_beds": total_occupied,
                    "available_beds": total_avail,
                    "occupancy_rate": round((total_occupied / total_cap * 100), 1) if total_cap else 0,
                    "ac_rooms": ac_rooms,
                    "non_ac_rooms": non_ac_rooms,
                    "active_students": active_students,
                    "vacated_students": vacated_students,
                    "pending_bookings": pending_bookings,
                    "vacating_requests": vacating_requests,
                    "pending_complaints": pending_complaints,
                    "resolved_complaints": resolved_complaints,
                    "total_revenue": total_revenue
                }
                self.send_json(stats)

            elif path == '/api/blocks':
                blocks = [
                    {"id": "Block A", "name": "Block A", "floors": 6, "gender": "Male", "rooms": 60, "capacity": 300, "incharge": "Mr. Suresh Nair", "contact": "9845112233"},
                    {"id": "Block B", "name": "Block B", "floors": 6, "gender": "Male", "rooms": 60, "capacity": 300, "incharge": "Mr. Ramesh Joshi", "contact": "9845112244"},
                    {"id": "Block C", "name": "Block C", "floors": 6, "gender": "Female", "rooms": 60, "capacity": 300, "incharge": "Dr. Sunita Rao", "contact": "9845112255"},
                    {"id": "Block D", "name": "Block D", "floors": 6, "gender": "Female", "rooms": 60, "capacity": 300, "incharge": "Mrs. Anita Deshmukh", "contact": "9845112266"}
                ]
                self.send_json(blocks)

            elif path == '/api/rooms':
                sql = "SELECT * FROM rooms WHERE 1=1"
                params = []
                if "block" in query and query["block"][0]:
                    sql += " AND block = ?"
                    params.append(query["block"][0])
                if "floor" in query and query["floor"][0]:
                    sql += " AND floor = ?"
                    params.append(int(query["floor"][0]))
                if "room_type" in query and query["room_type"][0]:
                    sql += " AND room_type = ?"
                    params.append(query["room_type"][0])
                if "bathroom_type" in query and query["bathroom_type"][0]:
                    sql += " AND bathroom_type = ?"
                    params.append(query["bathroom_type"][0])
                if "status" in query and query["status"][0]:
                    sql += " AND status = ?"
                    params.append(query["status"][0])
                if "search" in query and query["search"][0]:
                    s = f"%{query['search'][0]}%"
                    sql += " AND (id LIKE ? OR room_number LIKE ?)"
                    params.extend([s, s])

                sql += " ORDER BY block, floor, room_number"
                cur.execute(sql, params)
                rooms = []
                for row in cur.fetchall():
                    d = dict(row)
                    d["facilities"] = json.loads(d["facilities"]) if d["facilities"] else []
                    rooms.append(d)
                self.send_json(rooms)

            elif path.startswith('/api/rooms/'):
                room_id = path.split('/api/rooms/')[1]
                cur.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
                row = cur.fetchone()
                if row:
                    room = dict(row)
                    room["facilities"] = json.loads(room["facilities"]) if room["facilities"] else []
                    # Fetch student occupants
                    cur.execute("""
                    SELECT id, name, mobile, department, year, bed_number, checkin_date 
                    FROM users 
                    WHERE room_id = ? AND status = 'Active'
                    ORDER BY bed_number
                    """, (room_id,))
                    room["occupants"] = [dict(r) for r in cur.fetchall()]
                    self.send_json(room)
                else:
                    self.send_json({"error": "Room not found"}, 404)

            elif path == '/api/students':
                sql = "SELECT * FROM users WHERE role = 'student'"
                params = []
                if "status" in query and query["status"][0]:
                    sql += " AND status = ?"
                    params.append(query["status"][0])
                if "search" in query and query["search"][0]:
                    s = f"%{query['search'][0]}%"
                    sql += " AND (name LIKE ? OR email LIKE ? OR mobile LIKE ? OR room_id LIKE ?)"
                    params.extend([s, s, s, s])
                sql += " ORDER BY id DESC"
                cur.execute(sql, params)
                students = [dict(row) for row in cur.fetchall()]
                self.send_json(students)

            elif path.startswith('/api/students/'):
                stu_id = path.split('/api/students/')[1]
                cur.execute("SELECT * FROM users WHERE id = ?", (stu_id,))
                row = cur.fetchone()
                if row:
                    self.send_json(dict(row))
                else:
                    self.send_json({"error": "Student not found"}, 404)

            elif path == '/api/complaints':
                sql = "SELECT * FROM complaints WHERE 1=1"
                params = []
                if "student_id" in query and query["student_id"][0]:
                    sql += " AND student_id = ?"
                    params.append(query["student_id"][0])
                if "status" in query and query["status"][0]:
                    sql += " AND status = ?"
                    params.append(query["status"][0])
                if "category" in query and query["category"][0]:
                    sql += " AND category = ?"
                    params.append(query["category"][0])
                sql += " ORDER BY id DESC"
                cur.execute(sql, params)
                complaints = [dict(row) for row in cur.fetchall()]
                self.send_json(complaints)

            elif path == '/api/payments':
                sql = "SELECT * FROM payments WHERE 1=1"
                params = []
                if "student_id" in query and query["student_id"][0]:
                    sql += " AND student_id = ?"
                    params.append(query["student_id"][0])
                sql += " ORDER BY id DESC"
                cur.execute(sql, params)
                payments = [dict(row) for row in cur.fetchall()]
                self.send_json(payments)

            elif path == '/api/notices':
                cur.execute("SELECT * FROM notices ORDER BY date DESC, id DESC")
                notices = [dict(row) for row in cur.fetchall()]
                self.send_json(notices)

            else:
                self.send_json({"error": "Endpoint not found"}, 404)

        finally:
            conn.close()

    def handle_api_post(self, path, data):
        conn = get_db()
        cur = conn.cursor()

        try:
            if path == '/api/auth/send-otp':
                mobile = data.get('mobile')
                if not mobile or len(mobile) < 10:
                    self.send_json({"success": False, "error": "Invalid mobile number"}, 400)
                    return
                # Generate 6-digit OTP
                otp = str(random.randint(100000, 999999))
                OTP_STORE[mobile] = otp
                print(f"[OTP SERVICE] Sent OTP {otp} to mobile {mobile}")
                self.send_json({
                    "success": True,
                    "message": f"OTP successfully sent to +91 {mobile}.",
                    "demo_otp": otp  # Included for seamless demo testing without external SMS gateway
                })

            elif path == '/api/auth/verify-otp':
                mobile = data.get('mobile')
                entered_otp = data.get('otp')
                saved_otp = OTP_STORE.get(mobile)
                # Allow demo bypass '123456' as well as saved OTP
                if entered_otp == saved_otp or entered_otp == '123456':
                    self.send_json({"success": True, "message": "OTP verified successfully!"})
                else:
                    self.send_json({"success": False, "error": "Invalid or expired OTP. Please try again."}, 400)

            elif path == '/api/auth/login':
                email = data.get('email', '').strip().lower()
                password = data.get('password', '')
                cur.execute("SELECT * FROM users WHERE LOWER(email) = ? AND password = ?", (email, password))
                user_row = cur.fetchone()
                if user_row:
                    user_dict = dict(user_row)
                    user_dict.pop('password', None)
                    self.send_json({
                        "success": True,
                        "user": user_dict,
                        "token": f"jwt-token-{uuid.uuid4().hex[:12]}"
                    })
                else:
                    self.send_json({"success": False, "error": "Invalid email or password"}, 401)

            elif path == '/api/auth/register':
                email = data.get('email', '').strip().lower()
                cur.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
                if cur.fetchone():
                    self.send_json({"success": False, "error": "Email is already registered"}, 400)
                    return

                new_id = f"STU-{random.randint(100, 999)}"
                room_id = data.get('room_id')
                room_num = None
                floor_num = data.get('floor')
                block = data.get('block')

                # Bed capacity check if a room was directly requested
                if room_id:
                    cur.execute("SELECT occupied_beds, capacity, floor, block, room_number, status FROM rooms WHERE id = ?", (room_id,))
                    rm = cur.fetchone()
                    if rm:
                        if rm["status"] == "Maintenance":
                            self.send_json({"success": False, "error": "Selected room is under maintenance"}, 400)
                            return
                        if (rm["occupied_beds"] or 0) >= (rm["capacity"] or 5):
                            self.send_json({"success": False, "error": "Selected room is already fully occupied"}, 400)
                            return
                        room_num = rm["room_number"]
                        floor_num = rm["floor"]
                        block = rm["block"]

                status = "Pending Approval" if not room_id else "Active"
                bed_num = random.randint(1, 5) if room_id else None

                cur.execute("""
                INSERT INTO users (
                    id, name, email, password, role, mobile, gender, college, department,
                    year, parent_name, parent_contact, address, block, floor, room_id,
                    room_number, bed_number, room_type, bathroom_type, monthly_rent,
                    deposit_paid, checkin_date, status, id_proof, profile_photo
                ) VALUES (?, ?, ?, ?, 'student', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    new_id, data.get('name'), email, data.get('password', 'student123'),
                    data.get('mobile'), data.get('gender'), data.get('college'),
                    data.get('department'), data.get('year'), data.get('parent_name'),
                    data.get('parent_contact'), data.get('address'), block, floor_num,
                    room_id, room_num, bed_num, data.get('room_type', 'AC'),
                    data.get('bathroom_type', 'Attached'), data.get('monthly_rent', 8500),
                    data.get('deposit_paid', 0), data.get('checkin_date', datetime.now().strftime("%Y-%m-%d")),
                    status, data.get('id_proof', 'id_card.pdf'),
                    data.get('profile_photo', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80')
                ))

                if room_id and status == "Active":
                    cur.execute("UPDATE rooms SET occupied_beds = occupied_beds + 1 WHERE id = ?", (room_id,))
                    recalculate_room_status(cur, room_id)

                conn.commit()
                cur.execute("SELECT * FROM users WHERE id = ?", (new_id,))
                user_dict = dict(cur.fetchone())
                user_dict.pop('password', None)
                self.send_json({"success": True, "user": user_dict})

            elif path == '/api/bookings':
                # Direct booking submission
                student_id = data.get('student_id')
                room_id = data.get('room_id')

                cur.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
                rm = cur.fetchone()
                if not rm:
                    self.send_json({"success": False, "error": "Room not found"}, 404)
                    return
                if rm["status"] == "Maintenance":
                    self.send_json({"success": False, "error": "Room is under maintenance"}, 400)
                    return
                if (rm["occupied_beds"] or 0) >= (rm["capacity"] or 5):
                    self.send_json({"success": False, "error": "Room is fully occupied! Max 5 students allowed."}, 400)
                    return

                # Check if student already has an active room
                cur.execute("SELECT room_id, status FROM users WHERE id = ?", (student_id,))
                user = cur.fetchone()
                if not user:
                    self.send_json({"success": False, "error": "Student not found"}, 404)
                    return
                if user["room_id"] and user["status"] == "Active":
                    self.send_json({"success": False, "error": "You already have an allocated room. Vacate your current room first."}, 400)
                    return

                # Calculate next available bed number
                cur.execute("SELECT bed_number FROM users WHERE room_id = ? AND status = 'Active'", (room_id,))
                taken_beds = [r[0] for r in cur.fetchall() if r[0]]
                avail_beds = [b for b in range(1, 6) if b not in taken_beds]
                assigned_bed = avail_beds[0] if avail_beds else 1

                # Update user with room allocation
                cur.execute("""
                UPDATE users SET
                    room_id = ?, room_number = ?, block = ?, floor = ?,
                    room_type = ?, bathroom_type = ?, monthly_rent = ?,
                    bed_number = ?, status = 'Active', checkin_date = ?
                WHERE id = ?
                """, (
                    room_id, rm["room_number"], rm["block"], rm["floor"],
                    rm["room_type"], rm["bathroom_type"], rm["rent"],
                    assigned_bed, data.get('checkin_date', datetime.now().strftime("%Y-%m-%d")),
                    student_id
                ))

                # Increment room occupancy
                cur.execute("UPDATE rooms SET occupied_beds = occupied_beds + 1 WHERE id = ?", (room_id,))
                recalculate_room_status(cur, room_id)

                # Record deposit & rent initial payment record
                pay_id = f"PAY-{random.randint(100000, 999999)}"
                cur.execute("""
                INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Paid', ?, ?)
                """, (
                    pay_id, student_id, user["name"] if "name" in user.keys() else data.get("student_name", "Student"),
                    room_id, datetime.now().strftime("%B %Y"), rm["rent"], rm["deposit"],
                    f"Booking Rent ({rm['room_type']})", data.get("payment_method", "Online Payment"),
                    f"TXN-{random.randint(10000000, 99999999)}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    f"INV-{random.randint(1000, 9999)}"
                ))

                conn.commit()
                self.send_json({
                    "success": True,
                    "message": f"Room {room_id} booked successfully! Assigned Bed #{assigned_bed}.",
                    "bed_number": assigned_bed,
                    "room_id": room_id
                })

            elif path == '/api/complaints':
                cid = f"CMP-{random.randint(1005, 9999)}"
                cur.execute("""
                INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?, '', ?)
                """, (
                    cid, data.get('student_id'), data.get('student_name'), data.get('room_id'),
                    data.get('category'), data.get('title'), data.get('description'),
                    data.get('photo', ''), data.get('priority', 'Medium'),
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ))
                conn.commit()
                self.send_json({"success": True, "id": cid, "message": "Complaint lodged successfully!"})

            elif path.endswith('/vacate'):
                # Student vacating request
                stu_id = path.split('/api/students/')[1].split('/vacate')[0]
                leaving_date = data.get('vacating_date')
                reason = data.get('reason')
                cur.execute("""
                UPDATE users SET status = 'Vacating Requested', vacating_date = ?, vacating_reason = ?
                WHERE id = ?
                """, (leaving_date, reason, stu_id))
                conn.commit()
                self.send_json({"success": True, "message": "Vacating request submitted for admin review."})

            elif path == '/api/payments':
                pid = f"PAY-{random.randint(100000, 999999)}"
                cur.execute("""
                INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Paid', ?, ?)
                """, (
                    pid, data.get('student_id'), data.get('student_name'), data.get('room_id'),
                    data.get('month', datetime.now().strftime("%B %Y")),
                    data.get('amount'), data.get('deposit', 0), data.get('type', 'Monthly Rent'),
                    data.get('payment_method', 'Demo Payment Gateway'),
                    f"TXN-{random.randint(10000000, 99999999)}",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    f"INV-{datetime.now().year}-{random.randint(1000, 9999)}"
                ))
                conn.commit()
                self.send_json({"success": True, "payment_id": pid, "message": "Payment recorded successfully!"})

            elif path == '/api/notices':
                nid = f"NOT-{random.randint(10, 99)}"
                cur.execute("""
                INSERT INTO notices VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    nid, data.get('title'), data.get('category', 'General'),
                    data.get('priority', 'Normal'), data.get('author', 'Warden Office'),
                    data.get('content'), datetime.now().strftime("%Y-%m-%d")
                ))
                conn.commit()
                self.send_json({"success": True, "id": nid, "message": "Notice posted successfully."})

            elif path == '/api/rooms':
                # Admin adds new room
                rid = data.get('id')
                cur.execute("""
                INSERT INTO rooms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rid, data.get('block'), data.get('floor'), data.get('room_number'),
                    5, 0, 5, data.get('room_type', 'AC'), data.get('bathroom_type', 'Attached'),
                    data.get('rent', 8500), data.get('deposit', 10000), 'Available',
                    json.dumps(data.get('facilities', [])),
                    data.get('image', 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80'),
                    data.get('description', '')
                ))
                conn.commit()
                self.send_json({"success": True, "message": f"Room {rid} created successfully."})

            else:
                self.send_json({"error": "Unknown POST route"}, 404)

        finally:
            conn.close()

    def handle_api_put(self, path, data):
        conn = get_db()
        cur = conn.cursor()

        try:
            if path.startswith('/api/complaints/'):
                cid = path.split('/api/complaints/')[1]
                new_status = data.get('status')
                remarks = data.get('admin_remarks', '')
                cur.execute("""
                UPDATE complaints SET status = ?, admin_remarks = ? WHERE id = ?
                """, (new_status, remarks, cid))
                conn.commit()
                self.send_json({"success": True, "message": "Complaint updated successfully."})

            elif path.endswith('/approve-vacate'):
                # Admin approves student vacating -> decrement room occupancy and mark Vacated
                stu_id = path.split('/api/students/')[1].split('/approve-vacate')[0]
                cur.execute("SELECT room_id, status FROM users WHERE id = ?", (stu_id,))
                row = cur.fetchone()
                if row:
                    room_id = row["room_id"]
                    cur.execute("""
                    UPDATE users SET status = 'Vacated', room_id = NULL, room_number = NULL, bed_number = NULL
                    WHERE id = ?
                    """, (stu_id,))
                    
                    if room_id:
                        cur.execute("UPDATE rooms SET occupied_beds = MAX(0, occupied_beds - 1) WHERE id = ?", (room_id,))
                        recalculate_room_status(cur, room_id)
                        
                    conn.commit()
                    self.send_json({"success": True, "message": f"Vacating approved! Bed freed up in {room_id}."})
                else:
                    self.send_json({"error": "Student not found"}, 404)

            elif path.endswith('/approve-booking'):
                # Admin approves pending booking
                stu_id = path.split('/api/students/')[1].split('/approve-booking')[0]
                room_id = data.get('room_id')
                bed_number = data.get('bed_number', 1)
                
                cur.execute("UPDATE users SET status = 'Active', room_id = ?, bed_number = ? WHERE id = ?", (room_id, bed_number, stu_id))
                if room_id:
                    cur.execute("UPDATE rooms SET occupied_beds = occupied_beds + 1 WHERE id = ?", (room_id,))
                    recalculate_room_status(cur, room_id)
                conn.commit()
                self.send_json({"success": True, "message": "Student booking approved and bed allocated!"})

            elif path.startswith('/api/rooms/'):
                room_id = path.split('/api/rooms/')[1]
                status = data.get('status')
                rent = data.get('rent')
                cur.execute("UPDATE rooms SET status = ?, rent = ? WHERE id = ?", (status, rent, room_id))
                recalculate_room_status(cur, room_id)
                conn.commit()
                self.send_json({"success": True, "message": f"Room {room_id} updated."})

            else:
                self.send_json({"error": "Unknown PUT route"}, 404)

        finally:
            conn.close()

    def handle_api_delete(self, path):
        conn = get_db()
        cur = conn.cursor()
        try:
            if path.startswith('/api/notices/'):
                nid = path.split('/api/notices/')[1]
                cur.execute("DELETE FROM notices WHERE id = ?", (nid,))
                conn.commit()
                self.send_json({"success": True, "message": "Notice deleted."})
            elif path.startswith('/api/rooms/'):
                rid = path.split('/api/rooms/')[1]
                cur.execute("DELETE FROM rooms WHERE id = ?", (rid,))
                conn.commit()
                self.send_json({"success": True, "message": "Room deleted."})
            else:
                self.send_json({"error": "Unknown DELETE route"}, 404)
        finally:
            conn.close()

def run_server():
    # Ensure database exists
    if not os.path.exists(DB_PATH):
        print("Database not found, generating initial data...")
        import generate_data
        generate_data.init_all()

    handler = HostelRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("=" * 60)
        print("[HOSTEL MASTER] Hostel Booking and Management System")
        print(f"[*] Server running at http://localhost:{PORT}")
        print(f"[*] Access portal: http://localhost:{PORT}/index.html")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()
