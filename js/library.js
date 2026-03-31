// ============================================
// Library Module JavaScript
// ============================================

let currentTab = 'available';

document.addEventListener('DOMContentLoaded', () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return;
    }
    
    loadBooks();
    loadMyLoans();
    loadMyRequests();
    loadCategories();
});

async function loadBooks() {
    try {
        const books = await apiRequest('/library/books');
        displayBooks(books);
    } catch (error) {
        console.error('Error loading books:', error);
        document.getElementById('booksGrid').innerHTML = '<p class="text-center">Error loading books</p>';
    }
}

function displayBooks(books) {
    const grid = document.getElementById('booksGrid');
    
    if (books.length === 0) {
        grid.innerHTML = '<p class="text-center">No books available</p>';
        return;
    }
    
    grid.innerHTML = books.map(book => `
        <div class="book-card">
            <div class="book-cover">
                <i class="fas fa-book"></i>
            </div>
            <div class="book-info">
                <h3>${book.title}</h3>
                <p class="author">By ${book.author}</p>
                <span class="category">${book.category || 'General'}</span>
                <span class="availability ${book.available_copies > 0 ? 'available' : 'unavailable'}">
                    ${book.available_copies > 0 ? `${book.available_copies} available` : 'Not available'}
                </span>
                ${book.available_copies > 0 ? 
                    `<button class="btn-request" onclick="requestBook('${book.title}', '${book.author}')">
                        <i class="fas fa-request-book"></i> Request
                    </button>` : ''
                }
            </div>
        </div>
    `).join('');
}

async function searchBooks() {
    const query = document.getElementById('searchBooks').value;
    
    if (query.length < 2) {
        loadBooks();
        return;
    }
    
    try {
        const books = await apiRequest(`/library/books/search?q=${encodeURIComponent(query)}`);
        displayBooks(books);
    } catch (error) {
        console.error('Error searching books:', error);
    }
}

async function loadCategories() {
    try {
        const books = await apiRequest('/library/books');
        const categories = [...new Set(books.map(b => b.category).filter(Boolean))];
        
        const filter = document.getElementById('categoryFilter');
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            filter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function filterByCategory() {
    const category = document.getElementById('categoryFilter').value;
    
    if (!category) {
        loadBooks();
        return;
    }
    
    try {
        const books = await apiRequest('/library/books');
        const filtered = books.filter(b => b.category === category);
        displayBooks(filtered);
    } catch (error) {
        console.error('Error filtering books:', error);
    }
}

async function loadMyLoans() {
    try {
        const loans = await apiRequest('/library/loans/user');
        
        document.getElementById('currentLoansCount').textContent = loans.length;
        
        const totalFines = loans.reduce((sum, loan) => {
            if (loan.fine_amount) return sum + loan.fine_amount;
            const dueDate = new Date(loan.due_date);
            const today = new Date();
            if (dueDate < today) {
                const daysOverdue = Math.ceil((today - dueDate) / (1000 * 60 * 60 * 24));
                return sum + (daysOverdue * 50);
            }
            return sum;
        }, 0);
        
        document.getElementById('totalFines').textContent = `KES ${totalFines}`;
        
        const tbody = document.getElementById('myLoansTable');
        
        if (loans.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No active loans</td></tr>';
            return;
        }
        
        tbody.innerHTML = loans.map(loan => {
            const dueDate = new Date(loan.due_date);
            const today = new Date();
            const daysLeft = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
            let status = 'Active';
            let statusClass = 'status-active';
            let fine = 'KES 0';
            
            if (daysLeft < 0) {
                status = 'Overdue';
                statusClass = 'status-overdue';
                fine = `KES ${Math.abs(daysLeft) * 50}`;
            } else if (daysLeft <= 3) {
                status = 'Due Soon';
                statusClass = 'status-warning';
            }
            
            return `
                <tr>
                    <td>${loan.book_title}</td>
                    <td>${formatDate(loan.issue_date)}</td>
                    <td>${formatDate(loan.due_date)}</td>
                    <td><span class="status-badge ${statusClass}">${status}</span></td>
                    <td>${fine}</td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading loans:', error);
    }
}

async function loadMyRequests() {
    try {
        // For demo, show mock data
        const tbody = document.getElementById('myRequestsTable');
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center">No requests yet</td>
            </tr>
        `;
    } catch (error) {
        console.error('Error loading requests:', error);
    }
}

function requestBook(title, author) {
    document.getElementById('requestTitle').value = title;
    document.getElementById('requestAuthor').value = author;
    openModal('requestModal');
}

document.getElementById('requestForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const request = {
        title: document.getElementById('requestTitle').value,
        author: document.getElementById('requestAuthor').value,
        reason: document.getElementById('requestReason').value
    };
    
    // For demo, just show success
    showNotification('Book request submitted successfully!', 'success');
    closeModal('requestModal');
    e.target.reset();
});

function switchTab(tab) {
    currentTab = tab;
    
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(tab === 'available' ? 'available-books' : 
                         tab === 'myLoans' ? 'my-loans' : 'my-requests').classList.add('active');
}