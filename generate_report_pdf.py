import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = r"C:\Users\Ameen\.gemini\antigravity\scratch\hostel-booking-management-system\Hostel_Booking_and_Management_System_Project_Report.pdf"
ARTIFACT_PDF_PATH = r"C:\Users\Ameen\.gemini\antigravity\brain\01bedac3-2ef1-4b09-a241-e09f4ad4919c\Hostel_Booking_and_Management_System_Project_Report.pdf"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Suppress running header/footer on page 1 (Cover Page)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(54, 750, "HOSTEL BOOKING AND MANAGEMENT SYSTEM")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(612 - 54, 750, "Academic Mini Project Report")

            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

            # Footer
            self.line(54, 45, 612 - 54, 45)
            self.setFont("Helvetica", 8)
            self.drawString(54, 32, "HostelMaster • 4 Blocks • 240 Rooms • 1,200 Capacity")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 54, 32, page_text)
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1E3A8A")
    secondary_color = colors.HexColor("#0284C7")
    text_dark = colors.HexColor("#0F172A")
    text_muted = colors.HexColor("#475569")

    style_cover_dept = ParagraphStyle(
        'CoverDept',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#64748B"),
        alignment=1, # Center
        spaceAfter=6
    )

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=1,
        spaceAfter=12
    )

    style_cover_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=30
    )

    style_h1 = ParagraphStyle(
        'ReportH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'ReportH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=8
    )

    style_bullet = ParagraphStyle(
        'ReportBullet',
        parent=style_body,
        leftIndent=15,
        bulletIndent=5,
        spaceAfter=4
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", style_cover_dept))
    story.append(Paragraph("MINI PROJECT REPORT • ACADEMIC YEAR 2026–2027", style_cover_dept))
    story.append(Spacer(1, 40))

    story.append(Paragraph("HOSTEL BOOKING AND MANAGEMENT SYSTEM", style_cover_title))
    story.append(Paragraph("Automated Multi-Block Campus Residency, Bed Allotment & Student Welfare Portal", style_cover_sub))
    story.append(Spacer(1, 20))

    # Metric Badges Table
    badge_data = [
        [
            Paragraph("<b>4 BLOCKS</b><br/><font size=7 color='#64748b'>Blocks A, B, C, D</font>", style_body),
            Paragraph("<b>24 FLOORS</b><br/><font size=7 color='#64748b'>6 Floors per Block</font>", style_body),
            Paragraph("<b>240 ROOMS</b><br/><font size=7 color='#64748b'>10 Rooms per Floor</font>", style_body),
            Paragraph("<b>1,200 BEDS</b><br/><font size=7 color='#64748b'>5 Beds per Room</font>", style_body)
        ]
    ]
    t_badges = Table(badge_data, colWidths=[120, 120, 120, 120])
    t_badges.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_badges)
    story.append(Spacer(1, 100))

    # Project Details Footer
    footer_data = [
        [
            Paragraph("<b>Submitted By:</b><br/>Student Engineering Team<br/>GitHub: anoorul007-jpg", style_body),
            Paragraph("<b>Repository:</b><br/>github.com/anoorul007-jpg/<br/>hostel-booking-management-system", style_body),
            Paragraph("<b>Deployment Platform:</b><br/>Vercel Cloud Platform & GitHub<br/>Stack: HTML5, CSS3, JS, Python", style_body)
        ]
    ]
    t_footer = Table(footer_data, colWidths=[160, 180, 164])
    t_footer.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1.5, primary_color),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_footer)
    story.append(PageBreak())

    # ================= PAGE 2: ABSTRACT & PROBLEM STATEMENT =================
    story.append(Paragraph("Executive Summary & Abstract", style_h1))
    story.append(Paragraph(
        "Efficient student housing management is a vital operational prerequisite for modern academic universities. "
        "Traditional administrative approaches rely heavily on physical paper ledgers, fragmented notice boards, and "
        "manual entry registers. These legacy methods are susceptible to accidental double-bookings, delayed emergency responses, "
        "untracked room maintenance complaints, and lack of real-time vacancy visibility.",
        style_body
    ))
    story.append(Paragraph(
        "The <b>Hostel Booking and Management System (HostelMaster)</b> is a modern, responsive web application engineered "
        "to manage an expansive residential campus of <b>4 blocks (Blocks A, B, C, D)</b>, <b>24 floors</b>, and <b>240 rooms</b>, "
        "housing up to <b>1,200 students</b> in standardized 5-member sharing configurations.",
        style_body
    ))
    story.append(Paragraph(
        "The platform provides public registration with SMS OTP verification, an interactive 4-block visual floor explorer, "
        "real-time color-coded vacancy indicators (Green, Orange, Red, Grey), an online bed booking wizard with a demo payment gateway, "
        "a catalog of 14 core campus amenities, an 8-category grievance management portal with photo upload capabilities, "
        "a student dashboard with printable fee receipts, an automated vacating and bed replenishment workflow, and an administrator portal "
        "with live KPI analytics and CSV report generation.",
        style_body
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("1. System Architecture & Campus Scale", style_h1))
    story.append(Paragraph(
        "The hostel infrastructure is designed in a strict hierarchical layout:",
        style_body
    ))

    scale_table_data = [
        [Paragraph("Structural Entity", style_table_header), Paragraph("Quantity", style_table_header), Paragraph("Structural Details", style_table_header), Paragraph("Capacity Contribution", style_table_header)],
        [Paragraph("Blocks", style_table_cell), Paragraph("4 Blocks", style_table_cell), Paragraph("Block A & B (Boys), Block C & D (Girls)", style_table_cell), Paragraph("300 Beds per Block", style_table_cell)],
        [Paragraph("Floors", style_table_cell), Paragraph("24 Floors", style_table_cell), Paragraph("6 Floors per Block (Floors 1 to 6)", style_table_cell), Paragraph("50 Beds per Floor", style_table_cell)],
        [Paragraph("Rooms", style_table_cell), Paragraph("240 Rooms", style_table_cell), Paragraph("10 Rooms per Floor (Rooms 101 to 610)", style_table_cell), Paragraph("5 Beds per Room", style_table_cell)],
        [Paragraph("Total Capacity", style_table_cell), Paragraph("1,200 Beds", style_table_cell), Paragraph("Individual Bed Tracking (Bed #1 to #5)", style_table_cell), Paragraph("1,200 Students Max", style_table_cell)]
    ]
    t_scale = Table(scale_table_data, colWidths=[100, 75, 200, 129])
    t_scale.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_scale)

    story.append(Paragraph("Real-Time Color-Coded Room Indicators", style_h2))
    story.append(Paragraph("• <b>Green (Available):</b> Room is completely vacant (5 beds free).", style_bullet))
    story.append(Paragraph("• <b>Orange (Partially Occupied):</b> 1 to 4 beds occupied. Shows exact available bed positions.", style_bullet))
    story.append(Paragraph("• <b>Red (Fully Occupied):</b> All 5 beds occupied. New bookings are strictly prevented.", style_bullet))
    story.append(Paragraph("• <b>Grey (Maintenance):</b> Locked by administrator for repairs, painting, or sanitization.", style_bullet))
    story.append(PageBreak())

    # ================= PAGE 3: DATABASE SCHEMA =================
    story.append(Paragraph("2. Relational Database Design", style_h1))
    story.append(Paragraph(
        "The system uses an indexed SQLite database (<code>hostel.db</code>) with synchronized client-side local storage fallback "
        "to ensure instantaneous response times and zero downtime.",
        style_body
    ))

    db_data = [
        [Paragraph("Table", style_table_header), Paragraph("Primary Key", style_table_header), Paragraph("Key Attributes", style_table_header), Paragraph("Description", style_table_header)],
        [
            Paragraph("<b>rooms</b>", style_table_cell),
            Paragraph("id (TEXT)", style_table_cell),
            Paragraph("block, floor, room_number, capacity, occupied_beds, available_beds, room_type, bathroom_type, rent, deposit, status, facilities, image", style_table_cell),
            Paragraph("Stores inventory of all 240 rooms with real-time occupancy and rent rates.", style_table_cell)
        ],
        [
            Paragraph("<b>users</b>", style_table_cell),
            Paragraph("id (TEXT)", style_table_cell),
            Paragraph("name, email, password, role, mobile, gender, college, department, year, parent_name, parent_contact, room_id, bed_number, status", style_table_cell),
            Paragraph("Maintains credentials and resident profiles for students and administrative staff.", style_table_cell)
        ],
        [
            Paragraph("<b>complaints</b>", style_table_cell),
            Paragraph("id (TEXT)", style_table_cell),
            Paragraph("student_id, room_id, category, priority, title, description, photo, status, admin_remarks, created_at", style_table_cell),
            Paragraph("Tracks maintenance issues across 8 categories with photos and resolution notes.", style_table_cell)
        ],
        [
            Paragraph("<b>payments</b>", style_table_cell),
            Paragraph("id (TEXT)", style_table_cell),
            Paragraph("student_id, room_id, month, amount, deposit, payment_method, transaction_ref, status, invoice_no, payment_date", style_table_cell),
            Paragraph("Maintains transaction ledgers and data for printable tax receipts.", style_table_cell)
        ],
        [
            Paragraph("<b>notices</b>", style_table_cell),
            Paragraph("id (TEXT)", style_table_cell),
            Paragraph("title, category, priority, author, content, date", style_table_cell),
            Paragraph("Stores campus-wide announcements and emergency alerts.", style_table_cell)
        ]
    ]
    t_db = Table(db_data, colWidths=[75, 75, 214, 140])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_db)

    story.append(Spacer(1, 8))
    story.append(Paragraph("3. Core Functional Modules", style_h1))

    modules_data = [
        [Paragraph("Module", style_table_header), Paragraph("Key Features & Capabilities", style_table_header)],
        [
            Paragraph("<b>Interactive Room Explorer</b><br/>(rooms.html)", style_table_cell),
            Paragraph("Visual navigator toggles across 4 blocks and 6 floors. Shows real-time bed meters, AC/Non-AC badges, attached bathrooms, and bed layout modals with co-resident names.", style_table_cell)
        ],
        [
            Paragraph("<b>Registration & OTP</b><br/>(register.html)", style_table_cell),
            Paragraph("Student profile creation, guardian contacts, department, year, address, ID proof upload, and simulated SMS OTP verification with countdown timer.", style_table_cell)
        ],
        [
            Paragraph("<b>Bed Booking & Payments</b><br/>(booking.html)", style_table_cell),
            Paragraph("Enforces maximum 5-bed capacity, prevents double-booking, integrates demo payment gateway (UPI, Card, NetBanking), and generates printable tax receipts.", style_table_cell)
        ],
        [
            Paragraph("<b>14 Core Amenities</b><br/>(facilities.html)", style_table_cell),
            Paragraph("Showcases Wi-Fi (500 Mbps), CCTV, 24/7 security, RO drinking water, laundry, kitchen/dining, 24/7 study room, TV lounge, parking, generator backup, housekeeping, attached baths, hot water, and indoor/outdoor games.", style_table_cell)
        ],
        [
            Paragraph("<b>Complaint Management</b><br/>(complaints.html)", style_table_cell),
            Paragraph("8 categories (Water, Electricity, Wi-Fi, Cleaning, Maintenance, Food, Security, Other) with photo evidence upload and status tracking (Pending &rarr; In Progress &rarr; Resolved).", style_table_cell)
        ],
        [
            Paragraph("<b>Admin & Warden Portal</b><br/>(admin-dashboard.html)", style_table_cell),
            Paragraph("Live KPI metrics, room status manager, booking approvals, student directory, complaint resolution queue, circular broadcaster, and one-click CSV export.", style_table_cell)
        ]
    ]
    t_mod = Table(modules_data, colWidths=[140, 364])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_mod)
    story.append(PageBreak())

    # ================= PAGE 4: TESTING, DEPLOYMENT & CONCLUSION =================
    story.append(Paragraph("4. System Verification & Test Results", style_h1))
    story.append(Paragraph(
        "Automated regression and functional tests verified that all web routes, APIs, and business rules execute with zero failures:",
        style_body
    ))

    test_data = [
        [Paragraph("Test ID", style_table_header), Paragraph("Target Route / Module", style_table_header), Paragraph("Tested Condition", style_table_header), Paragraph("Result", style_table_header)],
        [Paragraph("TC-01", style_table_cell), Paragraph("/api/stats", style_table_cell), Paragraph("Verifies 4 blocks, 240 rooms, 1200 capacity metrics", style_table_cell), Paragraph("<font color='green'><b>PASS (200 OK)</b></font>", style_table_cell)],
        [Paragraph("TC-02", style_table_cell), Paragraph("/api/rooms?block=Block+A&floor=1", style_table_cell), Paragraph("Returns exact 10 rooms (101-110) with bed counts", style_table_cell), Paragraph("<font color='green'><b>PASS (200 OK)</b></font>", style_table_cell)],
        [Paragraph("TC-03", style_table_cell), Paragraph("Booking Allocation", style_table_cell), Paragraph("Enforces strict cap of 5 members per room", style_table_cell), Paragraph("<font color='green'><b>PASS (Blocked)</b></font>", style_table_cell)],
        [Paragraph("TC-04", style_table_cell), Paragraph("Double Booking Check", style_table_cell), Paragraph("Prevents student with active room from taking second room", style_table_cell), Paragraph("<font color='green'><b>PASS (Guarded)</b></font>", style_table_cell)],
        [Paragraph("TC-05", style_table_cell), Paragraph("Vacating Bed Release", style_table_cell), Paragraph("Approval decrements occupied beds and restores availability", style_table_cell), Paragraph("<font color='green'><b>PASS (Auto-freed)</b></font>", style_table_cell)],
        [Paragraph("TC-06", style_table_cell), Paragraph("Maintenance Toggle", style_table_cell), Paragraph("Setting room to Maintenance sets available beds to 0", style_table_cell), Paragraph("<font color='green'><b>PASS (Locked)</b></font>", style_table_cell)],
        [Paragraph("TC-07", style_table_cell), Paragraph("Receipt Generator", style_table_cell), Paragraph("Renders invoice breakdown with printable stylesheet", style_table_cell), Paragraph("<font color='green'><b>PASS (Rendered)</b></font>", style_table_cell)]
    ]
    t_test = Table(test_data, colWidths=[55, 145, 214, 90])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_test)

    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Deployment & Version Control", style_h1))
    story.append(Paragraph("• <b>GitHub Repository:</b> https://github.com/anoorul007-jpg/hostel-booking-management-system", style_bullet))
    story.append(Paragraph("• <b>Cloud Deployment:</b> Configured for Vercel with clean URL routing via <code>vercel.json</code>.", style_bullet))
    story.append(Paragraph("• <b>Local Server Execution:</b> Run via built-in Python server (<code>python server.py</code>) on <code>http://localhost:8080</code>.", style_bullet))
    story.append(Paragraph("• <b>VS Code Integration:</b> Pre-configured with launch configs (<code>.vscode/launch.json</code>) and one-click batch scripts.", style_bullet))

    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Conclusion & Future Scope", style_h1))
    story.append(Paragraph(
        "The <b>Hostel Booking and Management System</b> successfully replaces legacy paper-based housing registers with "
        "an automated, transparent, and scalable digital web portal. The system models 240 rooms across 4 residential blocks, "
        "empowering both students and administrators with granular bed control, maintenance visibility, and instant financial receipts.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Future Enhancements:</b> Planned upgrades include hardware integration with RFID turnstiles for biometric gate check-in, "
        "automated parent SMS notifications during curfew checkouts, and AI-driven predictive allocation based on academic branch compatibility.",
        style_body
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated PDF successfully at: {PDF_OUTPUT_PATH}")

    # Copy to artifacts directory
    import shutil
    shutil.copyfile(PDF_OUTPUT_PATH, ARTIFACT_PDF_PATH)
    print(f"Copied PDF to artifact directory: {ARTIFACT_PDF_PATH}")

if __name__ == "__main__":
    build_pdf()
