// ============================================
// Clubs Module JavaScript
// ============================================

let clubs = [];
let myClubs = [];

document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    
    loadClubs();
    loadEvents();
});

async function loadClubs() {
    try {
        // Mock data for demo
        clubs = [
            { id: 1, name: 'DevClub', description: 'Software development and coding club', category: 'Technology', members: 45, contact_email: 'devclub@omnicampus.edu', dues: 500 },
            { id: 2, name: 'Business Club', description: 'Entrepreneurship and business networking', category: 'Business', members: 32, contact_email: 'business@omnicampus.edu', dues: 300 },
            { id: 3, name: 'AI/ML Society', description: 'Artificial Intelligence and Machine Learning', category: 'Technology', members: 28, contact_email: 'aiml@omnicampus.edu', dues: 400 },
            { id: 4, name: 'Robotics Club', description: 'Build and program robots', category: 'Engineering', members: 25, contact_email: 'robotics@omnicampus.edu', dues: 600 }
        ];
        
        // Mock my clubs (user is a member of some clubs)
        myClubs = clubs.slice(0, 2);
        
        displayClubs();
        displayMyClubs();
    } catch (error) {
        console.error('Error loading clubs:', error);
    }
}

function displayClubs() {
    const grid = document.getElementById('clubsGrid');
    
    if (clubs.length === 0) {
        grid.innerHTML = '<p class="text-center">No clubs available</p>';
        return;
    }
    
    grid.innerHTML = clubs.map(club => {
        const isMember = myClubs.some(c => c.id === club.id);
        
        return `
            <div class="club-card">
                <div class="club-header">
                    <div class="club-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3>${club.name}</h3>
                </div>
                <p class="club-description">${club.description}</p>
                <div class="club-meta">
                    <span><i class="fas fa-tag"></i> ${club.category}</span>
                    <span><i class="fas fa-user-friends"></i> ${club.members} members</span>
                </div>
                <div class="club-actions">
                    ${isMember ? 
                        `<button class="btn-view" onclick="viewClub(${club.id})"><i class="fas fa-eye"></i> View</button>
                         <button class="btn-join" onclick="payDues(${club.id}, '${club.name}', ${club.dues})"><i class="fas fa-money-bill"></i> Pay Dues</button>` :
                        `<button class="btn-join" onclick="joinClub(${club.id})"><i class="fas fa-plus"></i> Join Club</button>
                         <button class="btn-view" onclick="viewClub(${club.id})"><i class="fas fa-eye"></i> View</button>`
                    }
                </div>
            </div>
        `;
    }).join('');
}

function displayMyClubs() {
    const grid = document.getElementById('myClubsGrid');
    
    if (myClubs.length === 0) {
        grid.innerHTML = '<p class="text-center">You haven\'t joined any clubs yet</p>';
        return;
    }
    
    grid.innerHTML = myClubs.map(club => `
        <div class="club-card">
            <div class="club-header">
                <div class="club-icon">
                    <i class="fas fa-users"></i>
                </div>
                <h3>${club.name}</h3>
            </div>
            <p class="club-description">${club.description}</p>
            <div class="club-meta">
                <span><i class="fas fa-tag"></i> ${club.category}</span>
                <span><i class="fas fa-user-friends"></i> ${club.members} members</span>
            </div>
            <div class="club-actions">
                <button class="btn-view" onclick="viewClub(${club.id})"><i class="fas fa-eye"></i> Details</button>
                <button class="btn-join" onclick="payDues(${club.id}, '${club.name}', ${club.dues})"><i class="fas fa-money-bill"></i> Pay Dues</button>
            </div>
        </div>
    `).join('');
}

function joinClub(clubId) {
    const club = clubs.find(c => c.id === clubId);
    if (club && !myClubs.some(c => c.id === clubId)) {
        myClubs.push(club);
        showNotification(`You've joined ${club.name}!`, 'success');
        displayClubs();
        displayMyClubs();
    }
}

function viewClub(clubId) {
    const club = clubs.find(c => c.id === clubId);
    
    const modalBody = document.getElementById('clubModalBody');
    modalBody.innerHTML = `
        <div class="club-details">
            <h3>${club.name}</h3>
            <p>${club.description}</p>
            
            <div class="details-grid">
                <div class="detail-item">
                    <label>Category</label>
                    <p>${club.category}</p>
                </div>
                <div class="detail-item">
                    <label>Members</label>
                    <p>${club.members}</p>
                </div>
                <div class="detail-item">
                    <label>Contact Email</label>
                    <p>${club.contact_email}</p>
                </div>
                <div class="detail-item">
                    <label>Annual Dues</label>
                    <p>KES ${club.dues}</p>
                </div>
            </div>
            
            <h4>Upcoming Events</h4>
            <div class="events-list">
                <div class="event-item">
                    <div class="event-date">Mar 15, 2025</div>
                    <div class="event-info">
                        <h5>Hackathon 2025</h5>
                        <p>Engineering Building, 9:00 AM</p>
                    </div>
                </div>
                <div class="event-item">
                    <div class="event-date">Mar 20, 2025</div>
                    <div class="event-info">
                        <h5>Workshop: Python for Beginners</h5>
                        <p>CS Lab 101, 2:00 PM</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    openModal('clubModal');
}

function payDues(clubId, clubName, amount) {
    document.getElementById('duesClubName').value = clubName;
    document.getElementById('duesAmount').value = amount;
    document.getElementById('duesAccount').textContent = `STUDENT-${Math.floor(Math.random() * 10000)}`;
    openModal('payDuesModal');
}

document.getElementById('payDuesForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    showNotification('Dues paid successfully!', 'success');
    closeModal('payDuesModal');
});

async function loadEvents() {
    try {
        const eventsList = document.getElementById('eventsList');
        eventsList.innerHTML = `
            <div class="event-card">
                <div class="event-date-badge">Mar 15</div>
                <div class="event-details">
                    <h3>Hackathon 2025</h3>
                    <p class="event-club">DevClub</p>
                    <p class="event-location"><i class="fas fa-map-marker-alt"></i> Engineering Building, 9:00 AM</p>
                    <p class="event-description">24-hour coding competition with prizes!</p>
                    <button class="btn-primary" onclick="rsvpEvent(1)"><i class="fas fa-check"></i> RSVP</button>
                </div>
            </div>
            <div class="event-card">
                <div class="event-date-badge">Mar 20</div>
                <div class="event-details">
                    <h3>Pitch Night</h3>
                    <p class="event-club">Business Club</p>
                    <p class="event-location"><i class="fas fa-map-marker-alt"></i> Business School, 6:00 PM</p>
                    <p class="event-description">Present your business ideas and get feedback</p>
                    <button class="btn-primary" onclick="rsvpEvent(2)"><i class="fas fa-check"></i> RSVP</button>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

function rsvpEvent(eventId) {
    showNotification('RSVP confirmed! Check your email for details.', 'success');
}

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    
    const contentId = tab === 'all-clubs' ? 'all-clubs' :
                     tab === 'my-clubs' ? 'my-clubs' : 'events';
    
    document.getElementById(contentId).classList.add('active');
}