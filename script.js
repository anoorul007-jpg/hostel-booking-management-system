/**
 * HOSTEL BOOKING AND MANAGEMENT SYSTEM
 * Unified Frontend Engine with Dual-Mode Architecture:
 * 1. REST API Client (when server.py is running)
 * 2. Persistent LocalDB fallback (when running directly in VS Code / Live Server)
 */

// ==========================================
// 1. DATABASE & STORAGE LAYER
// ==========================================
const HostelDB = {
  isBackendAvailable: null,

  async checkBackend() {
    if (this.isBackendAvailable !== null) return this.isBackendAvailable;
    try {
      const res = await fetch('/api/stats', { method: 'GET', headers: { 'Accept': 'application/json' } });
      this.isBackendAvailable = res.ok;
    } catch (e) {
      this.isBackendAvailable = false;
    }
    console.log(`[HostelDB] Operating Mode: ${this.isBackendAvailable ? 'REST API Server' : 'Standalone LocalDB'}`);
    return this.isBackendAvailable;
  },

  async initLocalStore() {
    if (!localStorage.getItem('hostel_data_initialized')) {
      try {
        const res = await fetch('initial_data.json');
        if (res.ok) {
          const data = await res.json();
          localStorage.setItem('hostel_rooms', JSON.stringify(data.rooms || []));
          localStorage.setItem('hostel_users', JSON.stringify([...(data.students || []), ...(data.admins || [])]));
          localStorage.setItem('hostel_complaints', JSON.stringify(data.complaints || []));
          localStorage.setItem('hostel_payments', JSON.stringify(data.payments || []));
          localStorage.setItem('hostel_notices', JSON.stringify(data.notices || []));
          localStorage.setItem('hostel_data_initialized', 'true');
          console.log('[HostelDB] Local store pre-seeded from initial_data.json');
          return;
        }
      } catch (err) {
        console.warn('[HostelDB] initial_data.json fetch failed, generating dynamically...', err);
      }
      this.generateFallbackData();
    }
  },

  generateFallbackData() {
    const blocks = ["Block A", "Block B", "Block C", "Block D"];
    const rooms = [];
    const images = [
      "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1540518614846-7ede433c4550?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80"
    ];

    blocks.forEach((block, bIdx) => {
      for (let floor = 1; floor <= 6; floor++) {
        for (let r = 1; r <= 10; r++) {
          const roomNum = floor * 100 + r;
          const roomId = `${block.replace(' ', '')}-${roomNum}`;
          const isAC = floor >= 4 || r % 2 === 0;
          const hasAttached = r <= 6;
          const baseRent = (isAC ? 8500 : 6000) + (hasAttached ? 1000 : 0);
          
          let status = "Partially Occupied";
          let occupied = (r % 4) + 1;
          if (r === 1 && floor === 1) { occupied = 0; status = "Available"; }
          if (r === 10) { occupied = 5; status = "Fully Occupied"; }
          if (roomId === "BlockA-105" || roomId === "BlockB-307") {
            occupied = 0;
            status = "Maintenance";
          }

          rooms.push({
            id: roomId,
            block,
            floor,
            room_number: roomNum,
            capacity: 5,
            occupied_beds: occupied,
            available_beds: status === "Maintenance" ? 0 : (5 - occupied),
            room_type: isAC ? "AC" : "Non-AC",
            bathroom_type: hasAttached ? "Attached" : "Common",
            rent: baseRent,
            deposit: 10000,
            status,
            facilities: [
              "High-Speed Wi-Fi",
              "Study Desk & Chair",
              "Personal Wardrobe",
              "Power Backup",
              ...(isAC ? ["Split Air Conditioner"] : []),
              ...(hasAttached ? ["Attached Western Bath", "24/7 Geyser Hot Water"] : ["Spacious Common Bath"])
            ],
            image: images[(floor + r) % images.length],
            description: `Modern 5-sharing ${isAC ? 'AC' : 'Non-AC'} room in ${block}, Floor ${floor}. Features ${hasAttached ? 'attached' : 'common'} bathroom and dedicated study area.`
          });
        }
      }
    });

    const users = [
      {
        id: "ADM-001",
        name: "Dr. Rajesh Verma",
        email: "admin@hostel.com",
        password: "admin123",
        role: "admin",
        mobile: "9811223344",
        department: "Chief Warden Office",
        status: "Active",
        profile_photo: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=300&q=80"
      },
      {
        id: "STU-001",
        name: "Rahul Sharma",
        email: "rahul@student.com",
        password: "student123",
        role: "student",
        mobile: "9876543210",
        gender: "Male",
        college: "National Institute of Tech",
        department: "Computer Science",
        year: "3rd Year",
        parent_name: "Satish Sharma",
        parent_contact: "9876543299",
        address: "42, Shanti Nagar, Jaipur",
        block: "Block A",
        floor: 2,
        room_id: "BlockA-201",
        room_number: 201,
        bed_number: 2,
        room_type: "AC",
        bathroom_type: "Attached",
        monthly_rent: 9500,
        deposit_paid: 10000,
        checkin_date: "2026-08-01",
        status: "Active",
        profile_photo: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=300&q=80"
      },
      {
        id: "STU-002",
        name: "Priya Patel",
        email: "priya@student.com",
        password: "student123",
        role: "student",
        mobile: "9876543211",
        gender: "Female",
        college: "State Tech University",
        department: "Electronics",
        year: "2nd Year",
        parent_name: "Mahesh Patel",
        parent_contact: "9876543298",
        address: "15, Navrangpura, Ahmedabad",
        block: "Block C",
        floor: 1,
        room_id: "BlockC-102",
        room_number: 102,
        bed_number: 1,
        room_type: "Non-AC",
        bathroom_type: "Attached",
        monthly_rent: 7000,
        deposit_paid: 10000,
        checkin_date: "2026-08-15",
        status: "Active",
        profile_photo: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=300&q=80"
      }
    ];

    const complaints = [
      {
        id: "CMP-1001",
        student_id: "STU-001",
        student_name: "Rahul Sharma",
        room_id: "BlockA-201",
        category: "Wi-Fi problems",
        title: "Intermittent Wi-Fi signal in room A-201",
        description: "The 5GHz Wi-Fi drops speed during evening study hours (8 PM - 10 PM).",
        status: "In Progress",
        priority: "High",
        admin_remarks: "Dual-band AP scheduled for installation on Floor 2.",
        created_at: "2026-11-10 14:30"
      }
    ];

    const payments = [
      {
        id: "PAY-882101",
        student_id: "STU-001",
        student_name: "Rahul Sharma",
        room_id: "BlockA-201",
        month: "November 2026",
        amount: 9500,
        deposit: 10000,
        type: "Monthly Rent (AC Attached)",
        payment_method: "UPI - PhonePe",
        transaction_ref: "UPI20261102987112",
        status: "Paid",
        payment_date: "2026-11-02 11:20:00",
        invoice_no: "INV-2026-11-001"
      }
    ];

    const notices = [
      {
        id: "NOT-01",
        title: "Annual Hostel Badminton & Table Tennis Tournament",
        category: "Event",
        priority: "Normal",
        author: "Warden Office",
        content: "Registrations open for Inter-Block Sports Championship starting this Saturday at indoor court.",
        date: "2026-11-13"
      },
      {
        id: "NOT-02",
        title: "Solar Hot Water Maintenance Schedule",
        category: "Maintenance",
        priority: "High",
        author: "Facilities Team",
        content: "Solar panels descaling scheduled on Sunday between 11 AM - 3 PM. Backup geysers will remain active.",
        date: "2026-11-12"
      }
    ];

    localStorage.setItem('hostel_rooms', JSON.stringify(rooms));
    localStorage.setItem('hostel_users', JSON.stringify(users));
    localStorage.setItem('hostel_complaints', JSON.stringify(complaints));
    localStorage.setItem('hostel_payments', JSON.stringify(payments));
    localStorage.setItem('hostel_notices', JSON.stringify(notices));
    localStorage.setItem('hostel_data_initialized', 'true');
  },

  // DATA METHODS
  async getStats() {
    if (await this.checkBackend()) {
      const res = await fetch('/api/stats');
      return await res.json();
    }
    await this.initLocalStore();
    const rooms = JSON.parse(localStorage.getItem('hostel_rooms') || '[]');
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    const complaints = JSON.parse(localStorage.getItem('hostel_complaints') || '[]');
    const payments = JSON.parse(localStorage.getItem('hostel_payments') || '[]');

    const totalRooms = rooms.length;
    const totalCap = rooms.reduce((acc, r) => acc + (r.capacity || 5), 0);
    const occupied = rooms.reduce((acc, r) => acc + (r.occupied_beds || 0), 0);
    const avail = rooms.reduce((acc, r) => acc + (r.available_beds || 0), 0);
    const acRooms = rooms.filter(r => r.room_type === 'AC').length;
    const nonAcRooms = rooms.filter(r => r.room_type === 'Non-AC').length;
    const activeStudents = users.filter(u => u.role === 'student' && u.status === 'Active').length;
    const pendingBookings = users.filter(u => u.role === 'student' && u.status === 'Pending Approval').length;
    const vacatingReqs = users.filter(u => u.role === 'student' && u.status === 'Vacating Requested').length;
    const pendingComplaints = complaints.filter(c => c.status !== 'Resolved').length;
    const resolvedComplaints = complaints.filter(c => c.status === 'Resolved').length;
    const totalRev = payments.filter(p => p.status === 'Paid').reduce((acc, p) => acc + (p.amount || 0), 0);

    return {
      total_blocks: 4,
      total_floors: 24,
      total_rooms: totalRooms,
      total_capacity: totalCap,
      occupied_beds: occupied,
      available_beds: avail,
      occupancy_rate: totalCap ? Math.round((occupied / totalCap) * 100) : 0,
      ac_rooms: acRooms,
      non_ac_rooms: nonAcRooms,
      active_students: activeStudents,
      pending_bookings: pendingBookings,
      vacating_requests: vacatingReqs,
      pending_complaints: pendingComplaints,
      resolved_complaints: resolvedComplaints,
      total_revenue: totalRev
    };
  },

  async getRooms(filters = {}) {
    if (await this.checkBackend()) {
      const q = new URLSearchParams(filters).toString();
      const res = await fetch(`/api/rooms?${q}`);
      return await res.json();
    }
    await this.initLocalStore();
    let rooms = JSON.parse(localStorage.getItem('hostel_rooms') || '[]');
    if (filters.block) rooms = rooms.filter(r => r.block === filters.block);
    if (filters.floor) rooms = rooms.filter(r => r.floor === parseInt(filters.floor));
    if (filters.room_type) rooms = rooms.filter(r => r.room_type === filters.room_type);
    if (filters.bathroom_type) rooms = rooms.filter(r => r.bathroom_type === filters.bathroom_type);
    if (filters.status) rooms = rooms.filter(r => r.status === filters.status);
    if (filters.search) {
      const s = filters.search.toLowerCase();
      rooms = rooms.filter(r => r.id.toLowerCase().includes(s) || r.room_number.toString().includes(s));
    }
    return rooms;
  },

  async getRoomById(id) {
    if (await this.checkBackend()) {
      const res = await fetch(`/api/rooms/${id}`);
      return await res.json();
    }
    await this.initLocalStore();
    const rooms = JSON.parse(localStorage.getItem('hostel_rooms') || '[]');
    const room = rooms.find(r => r.id === id);
    if (!room) return null;
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    room.occupants = users.filter(u => u.room_id === id && u.status === 'Active');
    return room;
  },

  async bookRoom(bookingData) {
    if (await this.checkBackend()) {
      const res = await fetch('/api/bookings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookingData)
      });
      return await res.json();
    }
    await this.initLocalStore();
    const rooms = JSON.parse(localStorage.getItem('hostel_rooms') || '[]');
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    const roomIdx = rooms.findIndex(r => r.id === bookingData.room_id);

    if (roomIdx === -1) return { success: false, error: "Room not found" };
    const room = rooms[roomIdx];
    if (room.status === "Maintenance") return { success: false, error: "Room is under maintenance" };
    if (room.occupied_beds >= room.capacity) return { success: false, error: "Room is fully occupied! Max 5 allowed." };

    const userIdx = users.findIndex(u => u.id === bookingData.student_id);
    if (userIdx === -1) return { success: false, error: "Student not found" };

    const occupants = users.filter(u => u.room_id === room.id && u.status === 'Active');
    const takenBeds = occupants.map(u => u.bed_number);
    let assignedBed = 1;
    for (let b = 1; b <= 5; b++) {
      if (!takenBeds.includes(b)) { assignedBed = b; break; }
    }

    users[userIdx].room_id = room.id;
    users[userIdx].room_number = room.room_number;
    users[userIdx].block = room.block;
    users[userIdx].floor = room.floor;
    users[userIdx].room_type = room.room_type;
    users[userIdx].bathroom_type = room.bathroom_type;
    users[userIdx].bed_number = assignedBed;
    users[userIdx].monthly_rent = room.rent;
    users[userIdx].status = 'Active';
    users[userIdx].checkin_date = bookingData.checkin_date || new Date().toISOString().split('T')[0];

    room.occupied_beds += 1;
    room.available_beds = Math.max(0, room.capacity - room.occupied_beds);
    room.status = room.occupied_beds >= room.capacity ? 'Fully Occupied' : 'Partially Occupied';

    // Record payment
    const payments = JSON.parse(localStorage.getItem('hostel_payments') || '[]');
    payments.unshift({
      id: `PAY-${Math.floor(100000 + Math.random() * 900000)}`,
      student_id: users[userIdx].id,
      student_name: users[userIdx].name,
      room_id: room.id,
      month: new Date().toLocaleString('default', { month: 'long', year: 'numeric' }),
      amount: room.rent,
      deposit: room.deposit,
      type: `Booking Rent (${room.room_type})`,
      payment_method: bookingData.payment_method || 'Online Payment',
      transaction_ref: `TXN-${Math.floor(10000000 + Math.random() * 90000000)}`,
      status: 'Paid',
      payment_date: new Date().toISOString().replace('T', ' ').substring(0, 19),
      invoice_no: `INV-${Math.floor(1000 + Math.random() * 9000)}`
    });

    localStorage.setItem('hostel_rooms', JSON.stringify(rooms));
    localStorage.setItem('hostel_users', JSON.stringify(users));
    localStorage.setItem('hostel_payments', JSON.stringify(payments));

    // Update current session user if same
    const cur = HostelAuth.getUser();
    if (cur && cur.id === users[userIdx].id) {
      localStorage.setItem('hostel_active_user', JSON.stringify(users[userIdx]));
    }

    return {
      success: true,
      message: `Room ${room.id} successfully booked! Allocated Bed #${assignedBed}.`,
      bed_number: assignedBed,
      room_id: room.id
    };
  },

  async vacateRoom(studentId, vacatingDate, reason) {
    if (await this.checkBackend()) {
      const res = await fetch(`/api/students/${studentId}/vacate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vacating_date: vacatingDate, reason })
      });
      return await res.json();
    }
    await this.initLocalStore();
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    const user = users.find(u => u.id === studentId);
    if (!user) return { success: false, error: "Student not found" };
    user.status = 'Vacating Requested';
    user.vacating_date = vacatingDate;
    user.vacating_reason = reason;
    localStorage.setItem('hostel_users', JSON.stringify(users));
    
    const cur = HostelAuth.getUser();
    if (cur && cur.id === studentId) {
      cur.status = 'Vacating Requested';
      localStorage.setItem('hostel_active_user', JSON.stringify(cur));
    }
    return { success: true, message: "Vacating request submitted for warden approval." };
  },

  async approveVacate(studentId) {
    if (await this.checkBackend()) {
      const res = await fetch(`/api/students/${studentId}/approve-vacate`, { method: 'PUT' });
      return await res.json();
    }
    await this.initLocalStore();
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    const rooms = JSON.parse(localStorage.getItem('hostel_rooms') || '[]');
    const user = users.find(u => u.id === studentId);
    if (!user) return { success: false, error: "Student not found" };

    const roomId = user.room_id;
    user.status = 'Vacated';
    user.room_id = null;
    user.room_number = null;
    user.bed_number = null;

    if (roomId) {
      const room = rooms.find(r => r.id === roomId);
      if (room) {
        room.occupied_beds = Math.max(0, room.occupied_beds - 1);
        room.available_beds = Math.min(room.capacity, room.capacity - room.occupied_beds);
        if (room.status !== 'Maintenance') {
          room.status = room.occupied_beds === 0 ? 'Available' : 'Partially Occupied';
        }
      }
    }

    localStorage.setItem('hostel_users', JSON.stringify(users));
    localStorage.setItem('hostel_rooms', JSON.stringify(rooms));
    return { success: true, message: `Vacating approved. Bed freed up in room ${roomId}.` };
  },

  async submitComplaint(data) {
    if (await this.checkBackend()) {
      const res = await fetch('/api/complaints', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      return await res.json();
    }
    await this.initLocalStore();
    const complaints = JSON.parse(localStorage.getItem('hostel_complaints') || '[]');
    const newId = `CMP-${Math.floor(1005 + Math.random() * 9000)}`;
    const comp = {
      id: newId,
      student_id: data.student_id,
      student_name: data.student_name,
      room_id: data.room_id,
      category: data.category,
      title: data.title,
      description: data.description,
      photo: data.photo || null,
      priority: data.priority || 'Medium',
      status: 'Pending',
      admin_remarks: '',
      created_at: new Date().toISOString().replace('T', ' ').substring(0, 16)
    };
    complaints.unshift(comp);
    localStorage.setItem('hostel_complaints', JSON.stringify(complaints));
    return { success: true, id: newId, message: "Complaint lodged successfully!" };
  },

  async updateComplaint(id, status, remarks) {
    if (await this.checkBackend()) {
      const res = await fetch(`/api/complaints/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status, admin_remarks: remarks })
      });
      return await res.json();
    }
    await this.initLocalStore();
    const complaints = JSON.parse(localStorage.getItem('hostel_complaints') || '[]');
    const comp = complaints.find(c => c.id === id);
    if (!comp) return { success: false, error: "Complaint not found" };
    comp.status = status;
    comp.admin_remarks = remarks || comp.admin_remarks;
    localStorage.setItem('hostel_complaints', JSON.stringify(complaints));
    return { success: true, message: "Complaint updated successfully." };
  },

  async getComplaints(filter = {}) {
    if (await this.checkBackend()) {
      const q = new URLSearchParams(filter).toString();
      const res = await fetch(`/api/complaints?${q}`);
      return await res.json();
    }
    await this.initLocalStore();
    let complaints = JSON.parse(localStorage.getItem('hostel_complaints') || '[]');
    if (filter.student_id) complaints = complaints.filter(c => c.student_id === filter.student_id);
    if (filter.status) complaints = complaints.filter(c => c.status === filter.status);
    if (filter.category) complaints = complaints.filter(c => c.category === filter.category);
    return complaints;
  },

  async getPayments(studentId = null) {
    if (await this.checkBackend()) {
      const q = studentId ? `?student_id=${studentId}` : '';
      const res = await fetch(`/api/payments${q}`);
      return await res.json();
    }
    await this.initLocalStore();
    let payments = JSON.parse(localStorage.getItem('hostel_payments') || '[]');
    if (studentId) payments = payments.filter(p => p.student_id === studentId);
    return payments;
  },

  async recordPayment(payData) {
    if (await this.checkBackend()) {
      const res = await fetch('/api/payments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payData)
      });
      return await res.json();
    }
    await this.initLocalStore();
    const payments = JSON.parse(localStorage.getItem('hostel_payments') || '[]');
    const newPay = {
      id: `PAY-${Math.floor(100000 + Math.random() * 900000)}`,
      student_id: payData.student_id,
      student_name: payData.student_name,
      room_id: payData.room_id,
      month: payData.month || new Date().toLocaleString('default', { month: 'long', year: 'numeric' }),
      amount: payData.amount,
      deposit: payData.deposit || 0,
      type: payData.type || 'Monthly Rent',
      payment_method: payData.payment_method || 'Online Gateway',
      transaction_ref: `TXN-${Math.floor(10000000 + Math.random() * 90000000)}`,
      status: 'Paid',
      payment_date: new Date().toISOString().replace('T', ' ').substring(0, 19),
      invoice_no: `INV-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`
    };
    payments.unshift(newPay);
    localStorage.setItem('hostel_payments', JSON.stringify(payments));
    return { success: true, payment_id: newPay.id, message: "Payment processed successfully!" };
  },

  async getNotices() {
    if (await this.checkBackend()) {
      const res = await fetch('/api/notices');
      return await res.json();
    }
    await this.initLocalStore();
    return JSON.parse(localStorage.getItem('hostel_notices') || '[]');
  },

  async addNotice(noticeData) {
    if (await this.checkBackend()) {
      const res = await fetch('/api/notices', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(noticeData)
      });
      return await res.json();
    }
    await this.initLocalStore();
    const notices = JSON.parse(localStorage.getItem('hostel_notices') || '[]');
    const newNotice = {
      id: `NOT-${Math.floor(10 + Math.random() * 90)}`,
      title: noticeData.title,
      category: noticeData.category || 'General',
      priority: noticeData.priority || 'Normal',
      author: noticeData.author || 'Warden Office',
      content: noticeData.content,
      date: new Date().toISOString().split('T')[0]
    };
    notices.unshift(newNotice);
    localStorage.setItem('hostel_notices', JSON.stringify(notices));
    return { success: true, id: newNotice.id };
  },

  async deleteNotice(id) {
    if (await this.checkBackend()) {
      const res = await fetch(`/api/notices/${id}`, { method: 'DELETE' });
      return await res.json();
    }
    await this.initLocalStore();
    let notices = JSON.parse(localStorage.getItem('hostel_notices') || '[]');
    notices = notices.filter(n => n.id !== id);
    localStorage.setItem('hostel_notices', JSON.stringify(notices));
    return { success: true };
  },

  async getStudents(filters = {}) {
    if (await this.checkBackend()) {
      const q = new URLSearchParams(filters).toString();
      const res = await fetch(`/api/students?${q}`);
      return await res.json();
    }
    await this.initLocalStore();
    let users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    let students = users.filter(u => u.role === 'student');
    if (filters.status) students = students.filter(s => s.status === filters.status);
    if (filters.search) {
      const s = filters.search.toLowerCase();
      students = students.filter(st =>
        (st.name && st.name.toLowerCase().includes(s)) ||
        (st.email && st.email.toLowerCase().includes(s)) ||
        (st.room_id && st.room_id.toLowerCase().includes(s))
      );
    }
    return students;
  }
};

// ==========================================
// 2. AUTHENTICATION SERVICE
// ==========================================
const HostelAuth = {
  getUser() {
    const raw = localStorage.getItem('hostel_active_user');
    return raw ? JSON.parse(raw) : null;
  },

  async login(email, password) {
    email = email.trim().toLowerCase();
    if (await HostelDB.checkBackend()) {
      try {
        const res = await fetch('/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (data.success && data.user) {
          localStorage.setItem('hostel_active_user', JSON.stringify(data.user));
          localStorage.setItem('hostel_token', data.token || 'demo-token');
          return { success: true, user: data.user };
        }
        return { success: false, error: data.error || "Login failed" };
      } catch (e) {
        console.warn('Backend login failed, fallback to local', e);
      }
    }

    await HostelDB.initLocalStore();
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    const user = users.find(u => u.email.toLowerCase() === email && u.password === password);
    if (user) {
      const safe = { ...user };
      delete safe.password;
      localStorage.setItem('hostel_active_user', JSON.stringify(safe));
      localStorage.setItem('hostel_token', 'local-token-xyz');
      return { success: true, user: safe };
    }
    return { success: false, error: "Invalid email or password" };
  },

  async register(formData) {
    if (await HostelDB.checkBackend()) {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (data.success && data.user) {
        localStorage.setItem('hostel_active_user', JSON.stringify(data.user));
        return { success: true, user: data.user };
      }
      return { success: false, error: data.error || "Registration failed" };
    }

    await HostelDB.initLocalStore();
    const users = JSON.parse(localStorage.getItem('hostel_users') || '[]');
    if (users.some(u => u.email.toLowerCase() === formData.email.toLowerCase())) {
      return { success: false, error: "Email already registered" };
    }

    const newId = `STU-${Math.floor(100 + Math.random() * 900)}`;
    const student = {
      id: newId,
      name: formData.name,
      email: formData.email,
      password: formData.password || 'student123',
      role: 'student',
      mobile: formData.mobile,
      gender: formData.gender,
      college: formData.college,
      department: formData.department,
      year: formData.year,
      parent_name: formData.parent_name,
      parent_contact: formData.parent_contact,
      address: formData.address,
      block: formData.block,
      floor: formData.floor ? parseInt(formData.floor) : null,
      room_id: formData.room_id || null,
      room_number: formData.room_id ? parseInt(formData.room_id.split('-')[1]) : null,
      bed_number: formData.room_id ? Math.floor(1 + Math.random() * 5) : null,
      room_type: formData.room_type || 'AC',
      bathroom_type: formData.bathroom_type || 'Attached',
      monthly_rent: formData.monthly_rent || 8500,
      deposit_paid: 0,
      checkin_date: formData.checkin_date || new Date().toISOString().split('T')[0],
      status: formData.room_id ? 'Active' : 'Pending Approval',
      id_proof: formData.id_proof || 'id_proof.pdf',
      profile_photo: formData.profile_photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80'
    };

    users.push(student);
    localStorage.setItem('hostel_users', JSON.stringify(users));

    if (formData.room_id) {
      const rooms = JSON.parse(localStorage.getItem('hostel_rooms') || '[]');
      const r = rooms.find(rm => rm.id === formData.room_id);
      if (r) {
        r.occupied_beds += 1;
        r.available_beds = Math.max(0, r.capacity - r.occupied_beds);
        r.status = r.occupied_beds >= r.capacity ? 'Fully Occupied' : 'Partially Occupied';
        localStorage.setItem('hostel_rooms', JSON.stringify(rooms));
      }
    }

    const safe = { ...student };
    delete safe.password;
    localStorage.setItem('hostel_active_user', JSON.stringify(safe));
    return { success: true, user: safe };
  },

  logout() {
    localStorage.removeItem('hostel_active_user');
    localStorage.removeItem('hostel_token');
    window.location.href = 'login.html';
  },

  requireAuth(role = null) {
    const user = this.getUser();
    if (!user) {
      window.location.href = 'login.html';
      return null;
    }
    if (role && user.role !== role) {
      showToast(`Unauthorized. Redirecting to your dashboard...`, 'error');
      setTimeout(() => {
        window.location.href = user.role === 'admin' ? 'admin-dashboard.html' : 'student-dashboard.html';
      }, 1000);
      return null;
    }
    return user;
  }
};

// ==========================================
// 3. UI HELPERS & NOTIFICATIONS
// ==========================================
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  const icon = type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ℹ';
  toast.innerHTML = `<span><strong>${icon}</strong> ${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideInRight 0.3s ease reverse forwards';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

function updateNavAuthUI() {
  const navActions = document.querySelector('.nav-actions');
  if (!navActions) return;

  const user = HostelAuth.getUser();
  if (user) {
    const dashLink = user.role === 'admin' ? 'admin-dashboard.html' : 'student-dashboard.html';
    const roleBadge = user.role === 'admin' ? 'Admin' : 'Student';
    navActions.innerHTML = `
      <a href="${dashLink}" class="user-pill">
        <img src="${user.profile_photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=300&q=80'}" class="user-avatar-sm" alt="Avatar">
        <span>${user.name.split(' ')[0]} <small class="badge badge-ac">${roleBadge}</small></span>
      </a>
      <button onclick="HostelAuth.logout()" class="btn btn-sm btn-outline">Logout</button>
    `;
  } else {
    navActions.innerHTML = `
      <a href="login.html" class="btn btn-sm btn-secondary">Login</a>
      <a href="register.html" class="btn btn-sm btn-primary">Book a Bed</a>
    `;
  }
}

// Mobile Nav Toggle
document.addEventListener('DOMContentLoaded', () => {
  updateNavAuthUI();
  const toggleBtn = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('show');
    });
  }
});
