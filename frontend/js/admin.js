// ============================================
// OmniCampus Admin Module
// ============================================

// Wait for auth.js to load first
document.addEventListener('DOMContentLoaded', function() {
    console.log('Admin.js loaded');
    
    // Check authentication
    if (typeof requireAdmin === 'function') {
        if (!requireAdmin()) return;
    } else {
        // Fallback if auth.js not loaded
        if (!localStorage.getItem('omnicampus_logged_in')) {
            window.location.href = '../login.html';
            return;
        }
    }
    
    // Initialize admin panel
    initAdminPanel();
    loadDashboardData();
    loadLibraryData();
    loadLostFoundData();
    loadClubsData();
    loadMedicalData();
    loadUsersData();
    
    // Initialize chart
    initChart();
});

// Initialize admin panel
function initAdminPanel() {
    const user = getCurrentUser();
    if (!user) return;
    
    // Update welcome message
    document.getElementById('adminWelcome').textContent = `Welcome, ${user.name || 'Administrator'}`;
    
    // Update admin info in sidebar
    const adminInfo = document.getElementById('adminInfo');
    if (adminInfo) {
        let roleDisplay = user.role || 'Admin';
        roleDisplay = roleDisplay.replace('_', ' ').toUpperCase();
        
        adminInfo.innerHTML = `
            <p><strong>${user.name || 'Admin'}</strong></p>
            <p>${roleDisplay}</p>
        `;
    }
    
    // Build sidebar based on role
    buildSidebar();
}

// Build sidebar based on user role
function buildSidebar() {
    const sidebar = document.getElementById('adminSidebar');
    if (!sidebar) return;
    
    const modules = getAdminModules();
    
    const icons = {
        'dashboard': 'fa-home',
        'library': 'fa-book',
        'lostfound': 'fa-search',
        'clubs': 'fa-users',
        'medical': 'fa-hospital',
        'users': 'fa-user-graduate'
    };
    
    const names = {
        'dashboard': 'Dashboard',
        'library': 'Library Mgmt',
        'lostfound': 'Lost & Found',
        'clubs': 'Clubs Mgmt',
        'medical': 'Medical Mgmt',
        'users': 'Users'
    };
    
    let sidebarHtml = '';
    modules.forEach(module => {
        sidebarHtml += `
            <li class="${module === 'dashboard' ? 'active' : ''}">
                <a href="#" onclick="showSection('${module}'); return false;">
                    <i class="fas ${icons[module] || 'fa-cog'}"></i> ${names[module] || module}
                </a>
            </li>
        `;
    });
    
    // Add logout
    sidebarHtml += `
        <li>
            <a href="#" onclick="logout(); return false;">
                <i class="fas fa-sign-out-alt"></i> Logout
            </a>
        </li>
    `;
    
    sidebar.innerHTML = sidebarHtml;
}

// Show selected section
function showSection(section) {
    // Hide all sections
    document.querySelectorAll('.admin-section').forEach(s => s.classList.remove('active'));
    
    // Show selected section
    const sectionElement = document.getElementById(section + '-section');
    if (sectionElement) {
        sectionElement.classList.add('active');
    }
    
    // Update sidebar active state
    document.querySelectorAll('.sidebar-nav ul li').forEach(li => li.classList.remove('active'));
    
    // Find and activate the clicked link
    const links = document.querySelectorAll('.sidebar-nav ul li a');
    for (let link of links) {
        if (link.getAttribute('onclick')?.includes(section)) {
            link.parentElement.classList.add('active');
            break;
        }
    }
    
    // Update title
    const titles = {
        'dashboard': 'Admin Dashboard',
        'library': 'Library Management',
        'lostfound': 'Lost & Found Management',
        'clubs': 'Clubs Management',
        'medical': 'Medical Services Management',
        'users': 'User Management'
    };
    
    const titleElement = document.getElementById('sectionTitle');
    if (titleElement) {
        titleElement.textContent = titles[section] || 'Admin Dashboard';
    }
}

// Load dashboard data
function loadDashboardData() {
    // Update stats (mock data)
    document.getElementById('totalBooks').textContent = '24';
    document.getElementById('totalStudents').textContent = '156';
    document.getElementById('activeLoans').textContent = '18';
    document.getElementById('pendingRequests').textContent = '5';
}

// Initialize chart
function initChart() {
    const canvas = document.getElementById('adminChart');
    if (!canvas || typeof Chart === 'undefined') return;
    
    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Books Issued',
                data: [12, 19, 15, 17, 24, 8, 5],
                borderColor: '#003366',
                backgroundColor: 'rgba(0, 51, 102, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#333' }
                }
            },
            scales: {
                y: {
                    grid: { color: '#e0e0e0' },
                    ticks: { color: '#666' }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#666' }
                }
            }
        }
    });
}

// ========== Library Functions ==========
function loadLibraryData() {
    const tbody = document.getElementById('libraryBooksTable');
    if (!tbody) return;
    
    // Mock data
    const books = [
        { id: 1, title: 'Introduction to Algorithms', author: 'Thomas H. Cormen', category: 'Computer Science', total: 5, available: 3 },
        { id: 2, title: 'Clean Code', author: 'Robert C. Martin', category: 'Programming', total: 3, available: 2 },
        { id: 3, title: 'The Pragmatic Programmer', author: 'David Thomas', category: 'Programming', total: 4, available: 4 },
        { id: 4, title: 'Design Patterns', author: 'Erich Gamma', category: 'Software Engineering', total: 2, available: 1 }
    ];
    
    tbody.innerHTML = books.map(book => `
        <tr>
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.category}</td>
            <td>${book.total}</td>
            <td>${book.available}</td>
            <td>
                <button class="btn-secondary btn-small" onclick="editBook(${book.id})"><i class="fas fa-edit"></i></button>
                <button class="btn-secondary btn-small" onclick="deleteBook(${book.id})"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `).join('');
}

function addBook() {
    alert('Add Book - This would open a form');
}

function editBook(id) {
    alert(`Edit Book ${id}`);
}

function deleteBook(id) {
    if (confirm('Are you sure you want to delete this book?')) {
        alert(`Book ${id} deleted`);
    }
}

function searchLibrary() {
    const search = document.getElementById('librarySearch')?.value.toLowerCase() || '';
    const rows = document.querySelectorAll('#libraryBooksTable tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(search) ? '' : 'none';
    });
}

// ========== Lost & Found Functions ==========
function loadLostFoundData() {
    // Lost items
    const lostTbody = document.getElementById('lostItemsTable');
    if (lostTbody) {
        const lostItems = [
            { id: 1, item: 'Laptop Charger', student: 'John Doe', location: 'Library', date: '2025-03-10', status: 'lost' },
            { id: 2, item: 'Water Bottle', student: 'Jane Smith', location: 'Gym', date: '2025-03-12', status: 'lost' }
        ];
        
        lostTbody.innerHTML = lostItems.map(item => `
            <tr>
                <td>${item.item}</td>
                <td>${item.student}</td>
                <td>${item.location}</td>
                <td>${item.date}</td>
                <td><span class="status-badge status-overdue">lost</span></td>
                <td>
                    <button class="btn-secondary btn-small" onclick="verifyItem(${item.id})">Verify</button>
                </td>
            </tr>
        `).join('');
    }
    
    // Found items
    const foundTbody = document.getElementById('foundItemsTable');
    if (foundTbody) {
        const foundItems = [
            { id: 1, item: 'USB Drive', student: 'Mike Johnson', location: 'CS Lab', date: '2025-03-14', status: 'found' },
            { id: 2, item: 'Calculator', student: 'Sarah Wilson', location: 'Library', date: '2025-03-15', status: 'found' }
        ];
        
        foundTbody.innerHTML = foundItems.map(item => `
            <tr>
                <td>${item.item}</td>
                <td>${item.student}</td>
                <td>${item.location}</td>
                <td>${item.date}</td>
                <td><span class="status-badge status-active">found</span></td>
                <td>
                    <button class="btn-primary btn-small" onclick="markReturned(${item.id})">Mark Returned</button>
                </td>
            </tr>
        `).join('');
    }
    
    // Matches
    const matchesDiv = document.getElementById('matchesList');
    if (matchesDiv) {
        matchesDiv.innerHTML = `
            <div class="match-card">
                <h3>Potential Match</h3>
                <div class="match-items">
                    <div class="match-item">
                        <h4>Lost: USB Drive</h4>
                        <p>Student: John Doe</p>
                        <p>32GB SanDisk, black</p>
                    </div>
                    <div class="match-arrow">→</div>
                    <div class="match-item">
                        <h4>Found: USB Drive</h4>
                        <p>Student: Mike Johnson</p>
                        <p>32GB SanDisk, black</p>
                    </div>
                </div>
                <button class="btn-primary" onclick="confirmMatch(1, 1)">Confirm Match</button>
            </div>
        `;
    }
}

function switchLFTab(tab) {
    // Update tab buttons
    document.querySelectorAll('#lostfound-section .tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Update tab content
    document.querySelectorAll('#lostfound-section .admin-tab').forEach(t => t.classList.remove('active'));
    document.getElementById(`lf-${tab}`).classList.add('active');
}

function verifyItem(id) {
    alert(`Item ${id} verified`);
}

function markReturned(id) {
    alert(`Item ${id} marked as returned`);
}

function confirmMatch(lostId, foundId) {
    alert('Match confirmed! Both parties will be notified.');
}

// ========== Clubs Functions ==========
function loadClubsData() {
    const tbody = document.getElementById('clubsTable');
    if (!tbody) return;
    
    const clubs = [
        { id: 1, name: 'DevClub', category: 'Technology', members: 45, status: 'active' },
        { id: 2, name: 'Business Club', category: 'Business', members: 32, status: 'active' },
        { id: 3, name: 'AI/ML Society', category: 'Technology', members: 28, status: 'pending' }
    ];
    
    tbody.innerHTML = clubs.map(club => `
        <tr>
            <td>${club.name}</td>
            <td>${club.category}</td>
            <td>${club.members}</td>
            <td><span class="status-badge ${club.status === 'active' ? 'status-active' : 'status-warning'}">${club.status}</span></td>
            <td>
                <button class="btn-secondary btn-small" onclick="editClub(${club.id})"><i class="fas fa-edit"></i></button>
                ${club.status === 'pending' ? 
                    `<button class="btn-primary btn-small" onclick="approveClub(${club.id})">Approve</button>` : ''}
                <button class="btn-secondary btn-small" onclick="deleteClub(${club.id})"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `).join('');
}

function addClub() {
    alert('Add Club - This would open a form');
}

function editClub(id) {
    alert(`Edit Club ${id}`);
}

function approveClub(id) {
    alert(`Club ${id} approved`);
}

function deleteClub(id) {
    if (confirm('Are you sure you want to delete this club?')) {
        alert(`Club ${id} deleted`);
    }
}

// ========== Medical Functions ==========
function loadMedicalData() {
    // Doctors
    const doctorsTbody = document.getElementById('doctorsTable');
    if (doctorsTbody) {
        const doctors = [
            { id: 1, name: 'Dr. Sarah Johnson', specialty: 'General Medicine', available: true },
            { id: 2, name: 'Dr. Michael Chen', specialty: 'Dentistry', available: true },
            { id: 3, name: 'Dr. Emily Brown', specialty: 'Counseling', available: false }
        ];
        
        doctorsTbody.innerHTML = doctors.map(doc => `
            <tr>
                <td>${doc.name}</td>
                <td>${doc.specialty}</td>
                <td><span class="status-badge ${doc.available ? 'status-active' : 'status-warning'}">${doc.available ? 'Available' : 'Unavailable'}</span></td>
                <td>
                    <button class="btn-secondary btn-small" onclick="toggleDoctor(${doc.id})">Toggle Status</button>
                </td>
            </tr>
        `).join('');
    }
    
    // Appointments
    const appointmentsTbody = document.getElementById('appointmentsTable');
    if (appointmentsTbody) {
        appointmentsTbody.innerHTML = `
            <tr>
                <td>John Doe</td>
                <td>Dr. Sarah Johnson</td>
                <td>2025-03-20</td>
                <td>10:00 AM</td>
                <td><span class="status-badge status-active">Upcoming</span></td>
                <td>
                    <button class="btn-secondary btn-small" onclick="confirmAppointment()">Confirm</button>
                    <button class="btn-secondary btn-small" onclick="cancelAppointment()">Cancel</button>
                </td>
            </tr>
        `;
    }
    
    // Medications
    const medicationsTbody = document.getElementById('medicationsTable');
    if (medicationsTbody) {
        medicationsTbody.innerHTML = `
            <tr>
                <td>Paracetamol 500mg</td>
                <td>Pain relief, fever</td>
                <td>KES 50</td>
                <td><span class="status-badge status-active">In Stock</span></td>
                <td>
                    <button class="btn-secondary btn-small">Edit</button>
                </td>
            </tr>
            <tr>
                <td>Amoxicillin 250mg</td>
                <td>Antibiotic</td>
                <td>KES 120</td>
                <td><span class="status-badge status-active">In Stock</span></td>
                <td>
                    <button class="btn-secondary btn-small">Edit</button>
                </td>
            </tr>
        `;
    }
}

function switchMedicalTab(tab) {
    document.querySelectorAll('#medical-section .tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    document.querySelectorAll('#medical-section .admin-tab').forEach(t => t.classList.remove('active'));
    document.getElementById(`medical-${tab}`).classList.add('active');
}

function addDoctor() {
    alert('Add Doctor - This would open a form');
}

function toggleDoctor(id) {
    alert(`Doctor ${id} status toggled`);
}

function addMedication() {
    alert('Add Medication - This would open a form');
}

function confirmAppointment() {
    alert('Appointment confirmed');
}

function cancelAppointment() {
    alert('Appointment cancelled');
}

// ========== Users Functions ==========
function loadUsersData() {
    const tbody = document.getElementById('usersTable');
    if (!tbody) return;
    
    const users = [
        { id: 1, studentId: 'S001', name: 'John Doe', email: 'john@student.edu', phone: '123-456-7890', role: 'student', status: 'active' },
        { id: 2, studentId: 'S002', name: 'Jane Smith', email: 'jane@student.edu', phone: '098-765-4321', role: 'student', status: 'active' },
        { id: 3, studentId: 'S003', name: 'Mike Johnson', email: 'mike@student.edu', phone: '555-123-4567', role: 'student', status: 'active' }
    ];
    
    tbody.innerHTML = users.map(user => `
        <tr>
            <td>${user.studentId}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.phone}</td>
            <td><span class="status-badge status-returned">${user.role}</span></td>
            <td><span class="status-badge status-active">${user.status}</span></td>
            <td>
                <button class="btn-secondary btn-small" onclick="editUser(${user.id})"><i class="fas fa-edit"></i></button>
                <button class="btn-secondary btn-small" onclick="deleteUser(${user.id})"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `).join('');
}

function searchUsers() {
    const search = document.getElementById('userSearch')?.value.toLowerCase() || '';
    const rows = document.querySelectorAll('#usersTable tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(search) ? '' : 'none';
    });
}

function editUser(id) {
    alert(`Edit User ${id}`);
}

function deleteUser(id) {
    if (confirm('Are you sure you want to delete this user?')) {
        alert(`User ${id} deleted`);
    }
}

// Make functions globally available
window.showSection = showSection;
window.addBook = addBook;
window.editBook = editBook;
window.deleteBook = deleteBook;
window.searchLibrary = searchLibrary;
window.switchLFTab = switchLFTab;
window.verifyItem = verifyItem;
window.markReturned = markReturned;
window.confirmMatch = confirmMatch;
window.addClub = addClub;
window.editClub = editClub;
window.approveClub = approveClub;
window.deleteClub = deleteClub;
window.switchMedicalTab = switchMedicalTab;
window.addDoctor = addDoctor;
window.toggleDoctor = toggleDoctor;
window.addMedication = addMedication;
window.confirmAppointment = confirmAppointment;
window.cancelAppointment = cancelAppointment;
window.editUser = editUser;
window.deleteUser = deleteUser;
window.searchUsers = searchUsers;