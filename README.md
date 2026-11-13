# 🏢 Hostel Booking and Management System

A modern, professional, fully responsive **Hostel Booking and Management System** built with **HTML5, CSS3, JavaScript**, and a lightweight **Python SQLite REST backend**.

---

## 🏗️ 1. Hostel Building Architecture & Scale
- **4 Blocks:** Block A (Boys Alpha), Block B (Boys Beta), Block C (Girls Gamma), Block D (Girls Delta)
- **6 Floors** in each block (Floors 1 through 6)
- **10 Rooms** on each floor (101-110, 201-210, 301-310, 401-410, 501-510, 601-610)
- **5 Members (Beds)** per room (Bed #1 to Bed #5)
- **Total Capacity:** **240 rooms** and **1,200 students**!

---

## 🎨 2. Real-Time Color-Coded Room Status
- 🟢 **Green – Available:** All 5 beds vacant.
- 🟠 **Orange – Partially Occupied:** 1 to 4 beds occupied.
- 🔴 **Red – Fully Occupied:** All 5 beds occupied.
- ⚪ **Grey – Maintenance:** Room temporarily closed for repairs or renovation.

*Room availability and bed count automatically update whenever a student books, checks in, or vacates.*

---

## 🚀 3. Key Feature Highlights
1. **Interactive Room Navigator (`rooms.html`):** Select any of the 4 blocks, browse all 6 floors, and inspect all 10 rooms with live bed occupancy meters, AC/Non-AC badges, and attached/common bath specifications.
2. **Bed Booking Wizard (`booking.html`):** Choose specific room and pick exact vacant bed position (Beds 1-5), select check-in date, review pricing, and simulate payment via demo gateway with instant receipt generation.
3. **Student Registration with OTP (`register.html`):** Comprehensive onboarding with college, department, year, parent contact, permanent address, photo preview, ID proof upload, and simulated SMS OTP verification.
4. **14 Featured Facilities (`facilities.html`):** High-speed Wi-Fi, 240+ CCTV cameras, 24/7 security, RO drinking water, automated laundry, modern dining hall, 24/7 study room, TV lounge, RFID parking, 100% power backup, housekeeping, attached baths, hot water, and indoor/outdoor games.
5. **Complaint Management System (`complaints.html`):** Lodge complaints under 8 categories (Water, Electricity, Wi-Fi, Bathroom Cleaning, Room Maintenance, Food Quality, Security, Other) with photo evidence upload and live status tracking.
6. **Student Portal (`student-dashboard.html`):** View personal profile, allocated room, roommates list, payment ledger, download official receipts, file maintenance tickets, and submit official vacating notices.
7. **Administrator Dashboard (`admin-dashboard.html`):** Full hostel oversight with live KPI cards, room management (edit status, add rooms), student directory, booking approvals, complaint resolution, vacating approvals, announcement broadcasts, and CSV export.
8. **Automated Vacating System:** Students submit vacating requests with preferred leaving date; upon admin approval, student is marked as Vacated and their bed is automatically released back to the room's available count.

---

## 📂 4. Project Directory Structure
```text
hostel-booking-management-system/
│
├── index.html               # Modern landing page with live statistics and block overview
├── login.html               # Dual role login (Student vs Admin) with 1-click demo logins
├── register.html            # Public student registration with interactive OTP verification
├── rooms.html               # 4 Blocks x 6 Floors x 10 Rooms visual explorer & bed modal
├── booking.html             # Room and bed reservation wizard with demo payment gateway
├── facilities.html          # Detailed catalog of all 14 hostel amenities
├── complaints.html          # Complaint filing portal with photo upload & ticket tracker
├── student-dashboard.html   # Student residency dashboard, roommates, invoices, vacating
├── admin-dashboard.html     # Comprehensive Warden portal with 240 rooms control & stats
│
├── style.css                # Ultra-modern responsive stylesheet with CSS variables & print styles
├── script.js                # Unified frontend engine with dual-mode storage (REST API + LocalDB)
├── server.py                # Python HTTP server & REST API with SQLite (Standard library only)
├── generate_data.py         # Seed generator for 240 rooms, sample students, complaints, payments
├── hostel.db                # SQLite database storing rooms, users, complaints, payments, notices
├── initial_data.json        # Pre-seeded JSON dataset
│
├── run.bat                  # 1-Click Windows Batch launcher
├── run.ps1                  # 1-Click PowerShell launcher
├── .vscode/
│   ├── launch.json          # VS Code F5 Run configuration
│   ├── tasks.json           # VS Code Build & Launch Tasks
│   └── settings.json        # Live Server and Editor configurations
└── README.md                # Project documentation
```

---

## ⚡ 5. How to Run with VS Code

### Method 1: Using the Built-In Python Server (Recommended)
1. Open **VS Code**.
2. Click **File > Open Folder...** and select:
   ```text
   C:\Users\Ameen\.gemini\antigravity\scratch\hostel-booking-management-system
   ```
3. Open the built-in terminal in VS Code (`Ctrl + ~`) and run:
   ```bash
   python server.py
   ```
4. Open your browser and navigate to:
   ```text
   http://localhost:8080/index.html
   ```
5. Or simply press **`F5`** in VS Code to start debugging!

---

### Method 2: 1-Click Launcher (Windows)
Double-click `run.bat` in the project folder. It will start the server and open the portal in your browser automatically.

---

### Method 3: Using VS Code "Live Server" Extension
1. Install the **Live Server** extension in VS Code.
2. Right-click on `index.html` and click **"Open with Live Server"**.
3. The system's intelligent **dual-mode engine** will automatically run in local mode with all 240 rooms, sample accounts, and dynamic updates!

---

## 🔑 6. Demo Login Credentials

### Administrator / Chief Warden Account:
- **Email:** `admin@hostel.com`
- **Password:** `admin123`
- *Accesses the full administrative portal (`admin-dashboard.html`), managing 240 rooms, student approvals, complaints, and vacating requests.*

### Student Accounts:
1. **Rahul Sharma** (Block A, Floor 2, Room 201 - AC Attached)
   - **Email:** `rahul@student.com`
   - **Password:** `password123`
2. **Priya Patel** (Block C, Floor 1, Room 102 - Girls Wing)
   - **Email:** `priya@student.com`
   - **Password:** `password123`
3. **Amit Kumar** (Block B, Floor 4, Room 403 - Boys Wing)
   - **Email:** `amit@student.com`
   - **Password:** `password123`

*(You can also use the 1-Click Demo Fill buttons on `login.html` to instantly test any account!)*
