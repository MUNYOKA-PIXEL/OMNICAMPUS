// Medical Module JavaScript
// Handles all medical services functionality with API integration

const MEDICAL_API = `${API_BASE}/medical`;

// State management
let appointments = [];
let doctors = [];
let medications = [];
let prescriptions = [];
let medicalRecords = [];
let healthResources = [];

// Initialize module
document.addEventListener('DOMContentLoaded', function() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    
    loadDoctors();
    loadAppointments();
    loadMedications();
    loadResources();
    populateDoctors();
    setMinDate();
});

// ==================== API Functions ====================

async function loadAppointments() {
    try {
        // Get appointments from localStorage first (for demo)
        const storedAppointments = localStorage.getItem('medical_appointments');
        if (storedAppointments) {
            appointments = JSON.parse(storedAppointments);
        } else {
            // Initialize with demo data
            appointments = [
                { 
                    id: 1, 
                    service: 'General Checkup', 
                    doctor: 'Dr. Sarah Johnson', 
                    date: getFutureDate(3), 
                    time: '10:00', 
                    status: 'upcoming',
                    reason: 'Annual physical examination'
                },
                { 
                    id: 2, 
                    service: 'Dental', 
                    doctor: 'Dr. Michael Chen', 
                    date: getFutureDate(7), 
                    time: '14:30', 
                    status: 'upcoming',
                    reason: 'Teeth cleaning'
                }
            ];
            localStorage.setItem('medical_appointments', JSON.stringify(appointments));
        }
        
        displayAppointments();
        updateStats();
    } catch (error) {
        console.error('Error loading appointments:', error);
        showNotification('Failed to load appointments', 'error');
    }
}

async function loadDoctors() {
    try {
        const storedDoctors = localStorage.getItem('medical_doctors');
        if (storedDoctors) {
            doctors = JSON.parse(storedDoctors);
        } else {
            // Initialize with demo data
            doctors = [
                { 
                    id: 1, 
                    name: 'Dr. Sarah Johnson', 
                    specialty: 'General Medicine', 
                    available: true,
                    education: 'MD, Nairobi Medical School',
                    experience: '10 years',
                    languages: ['English', 'Swahili']
                },
                { 
                    id: 2, 
                    name: 'Dr. Michael Chen', 
                    specialty: 'Dentistry', 
                    available: true,
                    education: 'DDS, University of Nairobi',
                    experience: '8 years',
                    languages: ['English', 'Mandarin']
                },
                { 
                    id: 3, 
                    name: 'Dr. Emily Brown', 
                    specialty: 'Counseling', 
                    available: true,
                    education: 'PhD, Clinical Psychology',
                    experience: '12 years',
                    languages: ['English', 'French']
                },
                { 
                    id: 4, 
                    name: 'Dr. James Mwangi', 
                    specialty: 'Eye Care', 
                    available: true,
                    education: 'MBChB, Ophthalmology',
                    experience: '6 years',
                    languages: ['English', 'Swahili', 'Kikuyu']
                }
            ];
            localStorage.setItem('medical_doctors', JSON.stringify(doctors));
        }
        
        displayDoctors();
    } catch (error) {
        console.error('Error loading doctors:', error);
        showNotification('Failed to load doctors', 'error');
    }
}

async function loadMedications() {
    try {
        const storedMeds = localStorage.getItem('medical_medications');
        if (storedMeds) {
            medications = JSON.parse(storedMeds);
        } else {
            medications = [
                { id: 1, name: 'Paracetamol 500mg', description: 'Pain relief, fever', price: 50, available: true, category: 'Pain Relief' },
                { id: 2, name: 'Amoxicillin 250mg', description: 'Antibiotic', price: 120, available: true, category: 'Antibiotics' },
                { id: 3, name: 'Loratadine 10mg', description: 'Allergy relief', price: 80, available: true, category: 'Allergy' },
                { id: 4, name: 'Ibuprofen 400mg', description: 'Anti-inflammatory', price: 65, available: false, category: 'Pain Relief' },
                { id: 5, name: 'Vitamin C 1000mg', description: 'Immune support', price: 150, available: true, category: 'Supplements' },
                { id: 6, name: 'Cetirizine 10mg', description: 'Antihistamine', price: 70, available: true, category: 'Allergy' }
            ];
            localStorage.setItem('medical_medications', JSON.stringify(medications));
        }
        
        displayMedications();
    } catch (error) {
        console.error('Error loading medications:', error);
    }
}

async function loadPrescriptions() {
    try {
        const storedPrescriptions = localStorage.getItem('medical_prescriptions');
        if (storedPrescriptions) {
            prescriptions = JSON.parse(storedPrescriptions);
        } else {
            prescriptions = [
                { 
                    id: 1, 
                    medication: 'Amoxicillin 250mg', 
                    prescribedBy: 'Dr. Sarah Johnson', 
                    date: getPastDate(15), 
                    expires: getFutureDate(15), 
                    refills: 1,
                    instructions: 'Take one capsule twice daily with food',
                    status: 'active'
                },
                { 
                    id: 2, 
                    medication: 'Loratadine 10mg', 
                    prescribedBy: 'Dr. Michael Chen', 
                    date: getPastDate(30), 
                    expires: getFutureDate(30), 
                    refills: 2,
                    instructions: 'Take one tablet daily for allergies',
                    status: 'active'
                }
            ];
            localStorage.setItem('medical_prescriptions', JSON.stringify(prescriptions));
        }
        
        displayPrescriptions();
    } catch (error) {
        console.error('Error loading prescriptions:', error);
    }
}

async function loadMedicalRecords() {
    try {
        const storedRecords = localStorage.getItem('medical_records');
        if (storedRecords) {
            medicalRecords = JSON.parse(storedRecords);
        } else {
            medicalRecords = [
                { id: 1, date: getPastDate(60), type: 'Consultation', doctor: 'Dr. Emily Brown', diagnosis: 'Anxiety management', notes: 'Counseling session - coping strategies discussed' },
                { id: 2, date: getPastDate(30), type: 'Vaccination', doctor: 'Dr. Sarah Johnson', diagnosis: 'Preventive care', notes: 'Annual flu vaccine administered' },
                { id: 3, date: getPastDate(90), type: 'Lab Test', doctor: 'Dr. Sarah Johnson', diagnosis: 'Routine checkup', notes: 'Blood work - all results normal' },
                { id: 4, date: getPastDate(120), type: 'Dental Cleaning', doctor: 'Dr. Michael Chen', diagnosis: 'Preventive', notes: 'Regular cleaning, no cavities' }
            ];
            localStorage.setItem('medical_records', JSON.stringify(medicalRecords));
        }
        
        displayMedicalRecords();
        openModal('medicalRecordsModal');
    } catch (error) {
        console.error('Error loading medical records:', error);
    }
}

async function loadResources() {
    try {
        const storedResources = localStorage.getItem('health_resources');
        if (storedResources) {
            healthResources = JSON.parse(storedResources);
        } else {
            healthResources = [
                { id: 1, title: 'Mental Health Guide', description: 'Resources for stress management and wellness', category: 'Mental Health' },
                { id: 2, title: 'First Aid Tips', description: 'Basic first aid procedures for common injuries', category: 'Emergency' },
                { id: 3, title: 'Nutrition Guide', description: 'Healthy eating tips for students', category: 'Wellness' },
                { id: 4, title: 'Sexual Health', description: 'Confidential information and services', category: 'Health' },
                { id: 5, title: 'Sleep Hygiene', description: 'Tips for better sleep and rest', category: 'Wellness' }
            ];
            localStorage.setItem('health_resources', JSON.stringify(healthResources));
        }
        
        displayResources();
    } catch (error) {
        console.error('Error loading resources:', error);
    }
}

// ==================== Display Functions ====================

function displayAppointments() {
    const list = document.getElementById('appointmentsList');
    
    if (!list) return;
    
    const upcoming = appointments.filter(apt => apt.status === 'upcoming');
    const past = appointments.filter(apt => apt.status === 'past' || apt.status === 'completed');
    
    if (upcoming.length === 0 && past.length === 0) {
        list.innerHTML = '<p class="text-center">No appointments found</p>';
        return;
    }

    let html = '<h3>Upcoming Appointments</h3>';
    
    if (upcoming.length > 0) {
        html += upcoming.map(apt => `
            <div class="appointment-card upcoming" data-id="${apt.id}">
                <div class="appointment-date">
                    <span class="day">${new Date(apt.date).toLocaleDateString('en-US', { weekday: 'short' })}</span>
                    <span class="date">${new Date(apt.date).getDate()}</span>
                    <span class="month">${new Date(apt.date).toLocaleDateString('en-US', { month: 'short' })}</span>
                </div>
                <div class="appointment-details">
                    <h4>${apt.service}</h4>
                    <p><i class="fas fa-user-md"></i> ${apt.doctor}</p>
                    <p><i class="fas fa-clock"></i> ${formatTime(apt.time)}</p>
                    <p class="reason">${apt.reason || 'No reason provided'}</p>
                </div>
                <div class="appointment-actions">
                    <span class="status-badge status-active">Upcoming</span>
                    <button class="btn-secondary btn-small" onclick="rescheduleAppointment(${apt.id})">Reschedule</button>
                    <button class="btn-secondary btn-small" onclick="cancelAppointment(${apt.id})">Cancel</button>
                </div>
            </div>
        `).join('');
    } else {
        html += '<p class="text-center">No upcoming appointments</p>';
    }

    html += '<h3 style="margin-top: 2rem;">Past Appointments</h3>';
    
    if (past.length > 0) {
        html += past.map(apt => `
            <div class="appointment-card past" data-id="${apt.id}">
                <div class="appointment-date">
                    <span class="day">${new Date(apt.date).toLocaleDateString('en-US', { weekday: 'short' })}</span>
                    <span class="date">${new Date(apt.date).getDate()}</span>
                    <span class="month">${new Date(apt.date).toLocaleDateString('en-US', { month: 'short' })}</span>
                </div>
                <div class="appointment-details">
                    <h4>${apt.service}</h4>
                    <p><i class="fas fa-user-md"></i> ${apt.doctor}</p>
                    <p><i class="fas fa-clock"></i> ${formatTime(apt.time)}</p>
                    <p class="notes">${apt.notes || 'Visit completed'}</p>
                </div>
                <div class="appointment-actions">
                    <span class="status-badge status-returned">Completed</span>
                    <button class="btn-secondary btn-small" onclick="bookFollowUp('${apt.service}', '${apt.doctor}')">Book Follow-up</button>
                </div>
            </div>
        `).join('');
    } else {
        html += '<p class="text-center">No past appointments</p>';
    }

    list.innerHTML = html;
}

function displayDoctors() {
    const grid = document.getElementById('doctorsGrid');
    
    if (!grid) return;
    
    grid.innerHTML = doctors.map(doc => `
        <div class="doctor-card" data-id="${doc.id}">
            <div class="doctor-avatar">
                <i class="fas fa-user-md"></i>
            </div>
            <h3>${doc.name}</h3>
            <p class="specialty">${doc.specialty}</p>
            <p class="availability ${doc.available ? 'available' : 'unavailable'}">
                <i class="fas fa-${doc.available ? 'check-circle' : 'times-circle'}"></i>
                ${doc.available ? 'Available Today' : 'Not Available'}
            </p>
            <p class="languages"><i class="fas fa-language"></i> ${doc.languages.join(', ')}</p>
            <p><small>${doc.experience} experience</small></p>
            <button class="btn-primary btn-small" onclick="quickBook('${doc.name}')" ${!doc.available ? 'disabled' : ''}>
                <i class="fas fa-calendar-plus"></i> Book
            </button>
        </div>
    `).join('');
}

function displayMedications() {
    const grid = document.getElementById('medicationsGrid');
    
    if (!grid) return;
    
    grid.innerHTML = medications.map(med => `
        <div class="medication-card" data-id="${med.id}">
            <i class="fas fa-pills"></i>
            <h4>${med.name}</h4>
            <p>${med.description}</p>
            <p class="price">KES ${med.price}</p>
            <span class="availability ${med.available ? 'available' : 'unavailable'}">
                ${med.available ? 'In Stock' : 'Out of Stock'}
            </span>
        </div>
    `).join('');
}

function displayResources() {
    const grid = document.getElementById('resourcesGrid');
    
    if (!grid) return;
    
    grid.innerHTML = healthResources.map(res => `
        <div class="resource-card">
            <i class="fas fa-info-circle"></i>
            <h4>${res.title}</h4>
            <p>${res.description}</p>
            <button class="btn-secondary btn-small" onclick="viewResource('${res.id}')">Learn More</button>
        </div>
    `).join('');
}

function displayMedicalRecords() {
    const list = document.getElementById('medicalRecordsList');
    
    if (!list) return;
    
    if (medicalRecords.length === 0) {
        list.innerHTML = '<p class="text-center">No medical records found</p>';
        return;
    }
    
    list.innerHTML = medicalRecords.sort((a, b) => new Date(b.date) - new Date(a.date)).map(record => `
        <div class="record-item">
            <div class="record-date">
                <span class="year">${new Date(record.date).getFullYear()}</span>
                <span class="day-month">${new Date(record.date).getDate()} ${new Date(record.date).toLocaleDateString('en-US', { month: 'short' })}</span>
            </div>
            <div class="record-details">
                <h4>${record.type}</h4>
                <p><i class="fas fa-user-md"></i> ${record.doctor}</p>
                <p><i class="fas fa-stethoscope"></i> ${record.diagnosis || 'N/A'}</p>
                <p><i class="fas fa-notes-medical"></i> ${record.notes}</p>
            </div>
        </div>
    `).join('');
}

function displayPrescriptions() {
    const list = document.getElementById('prescriptionsList');
    
    if (!list) return;
    
    if (prescriptions.length === 0) {
        list.innerHTML = '<p class="text-center">No active prescriptions</p>';
        return;
    }
    
    list.innerHTML = prescriptions.map(pres => {
        const today = new Date();
        const expiry = new Date(pres.expires);
        const isExpired = expiry < today;
        
        return `
            <div class="prescription-card ${isExpired ? 'expired' : ''}">
                <h4><i class="fas fa-prescription"></i> ${pres.medication}</h4>
                <p><i class="fas fa-user-md"></i> Prescribed by: ${pres.prescribedBy}</p>
                <p><i class="fas fa-calendar"></i> Date: ${formatDate(pres.date)}</p>
                <p><i class="fas fa-hourglass-end"></i> Expires: ${formatDate(pres.expires)}</p>
                <p><i class="fas fa-sync"></i> Refills left: ${pres.refills}</p>
                <div class="instructions">
                    <i class="fas fa-info-circle"></i> ${pres.instructions}
                </div>
                ${!isExpired && pres.refills > 0 ? 
                    `<button class="btn-primary btn-small" onclick="requestRefill(${pres.id})">
                        <i class="fas fa-sync"></i> Request Refill
                    </button>` : 
                    `<span class="status-badge ${isExpired ? 'status-overdue' : 'status-warning'}">
                        ${isExpired ? 'Expired' : 'No refills left'}
                    </span>`
                }
            </div>
        `;
    }).join('');
}

function loadInsuranceInfo() {
    const modalBody = document.getElementById('insuranceInfo');
    const user = getCurrentUser();
    
    modalBody.innerHTML = `
        <div class="insurance-card">
            <i class="fas fa-id-card"></i>
            <h3>Campus Health Insurance</h3>
            <div class="insurance-detail">
                <span class="label">Policy Holder:</span>
                <span class="value">${user?.name || 'Student'}</span>
            </div>
            <div class="insurance-detail">
                <span class="label">Student ID:</span>
                <span class="value">${user?.studentId || 'STU001'}</span>
            </div>
            <div class="insurance-detail">
                <span class="label">Policy Number:</span>
                <span class="value">CHI-${Math.floor(Math.random() * 1000000)}</span>
            </div>
            <div class="insurance-detail">
                <span class="label">Coverage Period:</span>
                <span class="value">Jan 1, 2025 - Dec 31, 2025</span>
            </div>
            <div class="insurance-detail">
                <span class="label">Coverage Type:</span>
                <span class="value">Comprehensive</span>
            </div>
        </div>
        <button class="btn-primary" onclick="downloadInsuranceCard()">
            <i class="fas fa-download"></i> Download Insurance Card
        </button>
    `;
    
    openModal('insuranceModal');
}

// ==================== Appointment Functions ====================

function bookAppointment(event) {
    event.preventDefault();
    
    const newAppointment = {
        id: Date.now(),
        service: document.getElementById('serviceType').value,
        doctor: document.getElementById('doctorSelect').value,
        date: document.getElementById('appointmentDate').value,
        time: document.getElementById('appointmentTime').value,
        status: 'upcoming',
        reason: document.getElementById('visitReason').value || 'No reason provided'
    };
    
    appointments.push(newAppointment);
    localStorage.setItem('medical_appointments', JSON.stringify(appointments));
    
    showNotification('Appointment booked successfully!', 'success');
    closeModal('bookAppointmentModal');
    displayAppointments();
    updateStats();
    event.target.reset();
}

function rescheduleAppointment(id) {
    const appointment = appointments.find(a => a.id === id);
    if (!appointment) return;
    
    // Pre-fill the form
    document.getElementById('serviceType').value = appointment.service;
    document.getElementById('appointmentDate').value = appointment.date;
    document.getElementById('visitReason').value = appointment.reason;
    
    // Select the doctor
    const doctorSelect = document.getElementById('doctorSelect');
    for (let i = 0; i < doctorSelect.options.length; i++) {
        if (doctorSelect.options[i].value === appointment.doctor) {
            doctorSelect.selectedIndex = i;
            break;
        }
    }
    
    // Remove old appointment
    appointments = appointments.filter(a => a.id !== id);
    localStorage.setItem('medical_appointments', JSON.stringify(appointments));
    
    openModal('bookAppointmentModal');
    showNotification('Please select new date and time', 'info');
}

function cancelAppointment(id) {
    if (confirm('Are you sure you want to cancel this appointment?')) {
        appointments = appointments.filter(a => a.id !== id);
        localStorage.setItem('medical_appointments', JSON.stringify(appointments));
        showNotification('Appointment cancelled', 'info');
        displayAppointments();
        updateStats();
    }
}

function bookFollowUp(service, doctor) {
    document.getElementById('serviceType').value = service;
    
    const doctorSelect = document.getElementById('doctorSelect');
    for (let i = 0; i < doctorSelect.options.length; i++) {
        if (doctorSelect.options[i].value === doctor) {
            doctorSelect.selectedIndex = i;
            break;
        }
    }
    
    document.getElementById('visitReason').value = 'Follow-up appointment';
    openModal('bookAppointmentModal');
}

function quickBook(doctorName) {
    const doctorSelect = document.getElementById('doctorSelect');
    for (let i = 0; i < doctorSelect.options.length; i++) {
        if (doctorSelect.options[i].value === doctorName) {
            doctorSelect.selectedIndex = i;
            break;
        }
    }
    openModal('bookAppointmentModal');
}

// ==================== Prescription Functions ====================

function requestRefill(prescriptionId) {
    const prescription = prescriptions.find(p => p.id === prescriptionId);
    if (!prescription) return;
    
    if (prescription.refills > 0) {
        prescription.refills -= 1;
        
        // Create refill request
        const refillRequest = {
            id: Date.now(),
            prescriptionId: prescriptionId,
            medication: prescription.medication,
            requestDate: new Date().toISOString(),
            status: 'pending'
        };
        
        // Store refill requests
        const refills = JSON.parse(localStorage.getItem('prescription_refills') || '[]');
        refills.push(refillRequest);
        localStorage.setItem('prescription_refills', JSON.stringify(refills));
        
        // Update prescriptions
        localStorage.setItem('medical_prescriptions', JSON.stringify(prescriptions));
        
        showNotification('Refill request sent to pharmacy. Ready in 2 hours.', 'success');
        displayPrescriptions();
    } else {
        showNotification('No refills remaining. Please contact your doctor.', 'error');
    }
}

// ==================== Helper Functions ====================

function populateDoctors() {
    const select = document.getElementById('doctorSelect');
    if (!select) return;
    
    // Clear existing options
    select.innerHTML = '<option value="">Select doctor</option>';
    
    doctors.forEach(doc => {
        if (doc.available) {
            const option = document.createElement('option');
            option.value = doc.name;
            option.textContent = `${doc.name} - ${doc.specialty}`;
            select.appendChild(option);
        }
    });
}

function setMinDate() {
    const dateInput = document.getElementById('appointmentDate');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;
    }
}

function updateStats() {
    const upcomingCount = appointments.filter(apt => apt.status === 'upcoming').length;
    const pastCount = appointments.filter(apt => apt.status === 'past' || apt.status === 'completed').length;
    const activePrescriptions = prescriptions.filter(p => {
        const expiry = new Date(p.expires);
        return expiry > new Date();
    }).length;
    
    document.getElementById('upcomingAppointments').textContent = upcomingCount;
    document.getElementById('pastAppointments').textContent = pastCount;
    document.getElementById('prescriptions').textContent = activePrescriptions;
}

function emergencyAlert() {
    const confirmed = confirm('EMERGENCY: This will alert campus security. Are you sure you need immediate assistance?');
    if (confirmed) {
        showNotification('🚨 EMERGENCY ALERT SENT! Help is on the way.', 'emergency');
        
        // Log emergency
        const emergencies = JSON.parse(localStorage.getItem('emergency_alerts') || '[]');
        emergencies.push({
            id: Date.now(),
            timestamp: new Date().toISOString(),
            user: getCurrentUser()?.name || 'Unknown'
        });
        localStorage.setItem('emergency_alerts', JSON.stringify(emergencies));
    }
}

function downloadInsuranceCard() {
    showNotification('Insurance card downloaded!', 'success');
}

function viewResource(resourceId) {
    const resource = healthResources.find(r => r.id == resourceId);
    if (resource) {
        showNotification(`Opening: ${resource.title}`, 'info');
    }
}

function formatTime(time) {
    const [hours, minutes] = time.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour % 12 || 12;
    return `${hour12}:${minutes} ${ampm}`;
}

function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function getFutureDate(days) {
    const date = new Date();
    date.setDate(date.getDate() + days);
    return date.toISOString().split('T')[0];
}

function getPastDate(days) {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString().split('T')[0];
}

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    
    const contentId = tab === 'appointments' ? 'appointments-tab' :
                     tab === 'doctors' ? 'doctors-tab' :
                     tab === 'pharmacy' ? 'pharmacy-tab' : 'resources-tab';
    
    document.getElementById(contentId).classList.add('active');
}

// ==================== Modal Functions ====================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Form submission
document.getElementById('appointmentForm')?.addEventListener('submit', bookAppointment);

// Export functions for global use
window.openModal = openModal;
window.closeModal = closeModal;
window.emergencyAlert = emergencyAlert;
window.switchTab = switchTab;
window.loadMedicalRecords = loadMedicalRecords;
window.loadPrescriptions = loadPrescriptions;
window.loadInsuranceInfo = loadInsuranceInfo;
window.rescheduleAppointment = rescheduleAppointment;
window.cancelAppointment = cancelAppointment;
window.bookFollowUp = bookFollowUp;
window.quickBook = quickBook;
window.requestRefill = requestRefill;
window.downloadInsuranceCard = downloadInsuranceCard;
window.viewResource = viewResource;