// ============================================
// Lost & Found Module JavaScript
// ============================================

let lostItems = [];
let foundItems = [];

document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    
    loadItems();
    loadMatches();
});

async function loadItems() {
    try {
        // Mock data for demo
        lostItems = [
            { id: 1, item_name: 'Laptop Charger', description: 'Dell laptop charger, black', category: 'Electronics', location_lost: 'Library 2nd Floor', date_lost: '2025-03-10', status: 'lost', user_name: 'John Doe' },
            { id: 2, item_name: 'Water Bottle', description: 'Blue Hydro Flask, 32oz', category: 'Accessories', location_lost: 'Gym', date_lost: '2025-03-12', status: 'lost', user_name: 'Jane Smith' }
        ];
        
        foundItems = [
            { id: 1, item_name: 'USB Drive', description: '32GB SanDisk, black', category: 'Electronics', location_found: 'CS Lab', date_found: '2025-03-14', status: 'found', user_name: 'Mike Johnson' }
        ];
        
        displayItems();
        updateStats();
    } catch (error) {
        console.error('Error loading items:', error);
    }
}

function displayItems() {
    const tbody = document.getElementById('itemsTable');
    const allItems = [
        ...lostItems.map(i => ({ ...i, type: 'lost', date: i.date_lost, location: i.location_lost })),
        ...foundItems.map(i => ({ ...i, type: 'found', date: i.date_found, location: i.location_found }))
    ].sort((a, b) => new Date(b.date) - new Date(a.date));
    
    tbody.innerHTML = allItems.map(item => `
        <tr>
            <td><span class="status-badge ${item.type === 'lost' ? 'status-overdue' : 'status-active'}">${item.type.toUpperCase()}</span></td>
            <td>${item.item_name}</td>
            <td>${item.description}</td>
            <td>${item.location}</td>
            <td>${formatDate(item.date)}</td>
            <td><span class="status-badge status-${item.type}">${item.status}</span></td>
            <td>
                ${item.type === 'found' ? 
                    `<button class="btn-secondary" onclick="claimItem(${item.id})">Claim</button>` : ''
                }
            </td>
        </tr>
    `).join('');
}

function updateStats() {
    document.getElementById('lostCount').textContent = lostItems.length;
    document.getElementById('foundCount').textContent = foundItems.length;
    document.getElementById('matchCount').textContent = '0';
    document.getElementById('recoveryRate').textContent = '75%';
}

function filterItems() {
    const search = document.getElementById('searchItems').value.toLowerCase();
    const rows = document.querySelectorAll('#itemsTable tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(search) ? '' : 'none';
    });
}

function claimItem(id) {
    showNotification('Claim request submitted! Admin will review it.', 'success');
}

document.getElementById('lostForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const newItem = {
        item_name: document.getElementById('lostItemName').value,
        category: document.getElementById('lostCategory').value,
        description: document.getElementById('lostDescription').value,
        location_lost: document.getElementById('lostLocation').value,
        date_lost: document.getElementById('lostDate').value
    };
    
    lostItems.push({ ...newItem, id: Date.now(), status: 'lost' });
    showNotification('Lost item reported successfully!', 'success');
    closeModal('reportLostModal');
    displayItems();
    updateStats();
    e.target.reset();
});

document.getElementById('foundForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const newItem = {
        item_name: document.getElementById('foundItemName').value,
        category: document.getElementById('foundCategory').value,
        description: document.getElementById('foundDescription').value,
        location_found: document.getElementById('foundLocation').value,
        date_found: document.getElementById('foundDate').value
    };
    
    foundItems.push({ ...newItem, id: Date.now(), status: 'found' });
    showNotification('Found item reported successfully!', 'success');
    closeModal('reportFoundModal');
    displayItems();
    updateStats();
    e.target.reset();
});

function loadMatches() {
    // Check for potential matches
    const matches = [];
    
    lostItems.forEach(lost => {
        foundItems.forEach(found => {
            if (lost.category === found.category &&
                (lost.item_name.toLowerCase().includes(found.item_name.toLowerCase()) ||
                 found.item_name.toLowerCase().includes(lost.item_name.toLowerCase()))) {
                matches.push({ lost, found });
            }
        });
    });
    
    const matchCount = document.getElementById('matchCount');
    if (matchCount) {
        matchCount.textContent = matches.length;
    }
}

function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    
    const contentId = tab === 'all' ? 'all-items' :
                     tab === 'lost' ? 'lost-items' :
                     tab === 'found' ? 'found-items' :
                     tab === 'matches' ? 'matches-items' : 'my-reports';
    
    document.getElementById(contentId).classList.add('active');
    
    if (tab === 'matches') {
        displayMatches();
    }
}

function displayMatches() {
    const matchesGrid = document.getElementById('matchesGrid');
    
    const matches = [];
    lostItems.forEach(lost => {
        foundItems.forEach(found => {
            if (lost.category === found.category) {
                matches.push(`
                    <div class="match-card">
                        <h3>Potential Match Found!</h3>
                        <div class="match-items">
                            <div class="match-item">
                                <h4>Lost Item</h4>
                                <p><strong>${lost.item_name}</strong></p>
                                <p>${lost.description}</p>
                                <p>Location: ${lost.location_lost}</p>
                                <p>Date: ${formatDate(lost.date_lost)}</p>
                            </div>
                            <div class="match-arrow">
                                <i class="fas fa-arrow-right"></i>
                            </div>
                            <div class="match-item">
                                <h4>Found Item</h4>
                                <p><strong>${found.item_name}</strong></p>
                                <p>${found.description}</p>
                                <p>Location: ${found.location_found}</p>
                                <p>Date: ${formatDate(found.date_found)}</p>
                            </div>
                        </div>
                        <button class="btn-primary" onclick="notifyMatch()">Notify Admin</button>
                    </div>
                `);
            }
        });
    });
    
    matchesGrid.innerHTML = matches.length ? matches.join('') : 
        '<p class="text-center">No matches found yet</p>';
}

function notifyMatch() {
    showNotification('Admin notified about potential match!', 'success');
}