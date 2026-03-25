// ============================================
// OmniCampus Authentication Module
// ============================================

// Check if user is authenticated
function isAuthenticated() {
    const loggedIn = localStorage.getItem('omnicampus_logged_in');
    return loggedIn === 'true';
}

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem('omnicampus_user');
    if (!userStr) return null;
    
    try {
        return JSON.parse(userStr);
    } catch (e) {
        console.error('Error parsing user data:', e);
        return null;
    }
}

// Get user role
function getUserRole() {
    const user = getCurrentUser();
    return user ? user.role : null;
}

// Check if current user is admin
function isAdmin() {
    const user = getCurrentUser();
    return user && (user.role === 'admin' || user.role.includes('_admin') || user.role === 'super_admin');
}

// Check if user has specific permission
function hasPermission(permission) {
    const user = getCurrentUser();
    if (!user) return false;
    
    // Super admin has all permissions
    if (user.role === 'super_admin' || user.role === 'admin') return true;
    
    // Get permissions from user object or localStorage
    const permissions = user.permissions || [];
    return permissions.includes(permission) || permissions.includes('all');
}

// Get admin modules based on role
function getAdminModules() {
    const user = getCurrentUser();
    if (!user) return ['dashboard'];
    
    // Check if modules are stored in localStorage
    const storedModules = localStorage.getItem('admin_modules');
    if (storedModules) {
        try {
            return JSON.parse(storedModules);
        } catch (e) {
            console.error('Error parsing admin modules:', e);
        }
    }
    
    // Default modules based on role
    switch(user.role) {
        case 'super_admin':
        case 'admin':
            return ['dashboard', 'library', 'lostfound', 'clubs', 'medical', 'users'];
        case 'library_admin':
            return ['dashboard', 'library'];
        case 'lost_found_admin':
            return ['dashboard', 'lostfound'];
        case 'clubs_admin':
            return ['dashboard', 'clubs'];
        case 'medical_admin':
            return ['dashboard', 'medical'];
        case 'user_admin':
            return ['dashboard', 'users'];
        default:
            return ['dashboard'];
    }
}

// Login function
function login(userData) {
    if (!userData) return false;
    
    // Ensure userData has required fields
    const user = {
        id: userData.id || 'user_' + Date.now(),
        name: userData.name || userData.username || 'User',
        email: userData.email || '',
        studentId: userData.studentId || userData.username || '',
        role: userData.role || 'student',
        loginTime: new Date().toISOString(),
        permissions: userData.permissions || []
    };
    
    localStorage.setItem('omnicampus_user', JSON.stringify(user));
    localStorage.setItem('omnicampus_logged_in', 'true');
    localStorage.setItem('omnicampus_login_time', Date.now().toString());
    
    return true;
}

// Logout function
function logout() {
    // Clear all OmniCampus related localStorage items
    localStorage.removeItem('omnicampus_user');
    localStorage.removeItem('omnicampus_logged_in');
    localStorage.removeItem('omnicampus_login_time');
    localStorage.removeItem('admin_modules');
    localStorage.removeItem('admin_data');
    
    // Redirect to login page
    window.location.href = 'login.html';
}

// Update user info in sidebar
function updateUserInfo() {
    const user = getCurrentUser();
    const userInfoElement = document.getElementById('userInfo');
    
    if (userInfoElement && user) {
        let roleDisplay = user.role || 'Student';
        if (roleDisplay.includes('_')) {
            roleDisplay = roleDisplay.split('_').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
        } else {
            roleDisplay = roleDisplay.charAt(0).toUpperCase() + roleDisplay.slice(1);
        }
        
        userInfoElement.innerHTML = `
            <p><strong>${user.name || user.studentId || 'User'}</strong></p>
            <p>${user.studentId ? `ID: ${user.studentId}` : ''}</p>
            <p><small>${roleDisplay}</small></p>
        `;
    }
}

// Redirect if not authenticated
function requireAuth(redirectUrl = 'login.html') {
    if (!isAuthenticated()) {
        window.location.href = redirectUrl;
        return false;
    }
    return true;
}

// Redirect if not admin
function requireAdmin(redirectUrl = 'login.html') {
    if (!isAuthenticated() || !isAdmin()) {
        window.location.href = redirectUrl;
        return false;
    }
    return true;
}

// Redirect based on role
function redirectToDashboard() {
    const user = getCurrentUser();
    if (!user) {
        window.location.href = 'login.html';
        return;
    }
    
    if (isAdmin()) {
        window.location.href = 'admin/index.html';
    } else {
        window.location.href = 'dashboard.html';
    }
}

// Initialize auth check on page load
document.addEventListener('DOMContentLoaded', function() {
    // Skip auth check for public pages
    const currentPath = window.location.pathname;
    const currentPage = currentPath.split('/').pop();
    const publicPages = ['login.html', 'register.html', 'index.html', ''];
    
    // Check if current page is public
    const isPublicPage = publicPages.includes(currentPage) || 
                         currentPath.endsWith('/') || 
                         currentPath.endsWith('index.html');
    
    if (isPublicPage) {
        // If user is already logged in on public page, show user info in navbar if element exists
        if (isAuthenticated()) {
            const userMenu = document.querySelector('.user-menu');
            if (userMenu) {
                const user = getCurrentUser();
                userMenu.innerHTML = `<span>Welcome, ${user.name || 'User'}</span>`;
            }
        }
        return;
    }
    
    // For protected pages, check authentication
    if (!requireAuth()) {
        return;
    }
    
    // Update user info in sidebar if element exists
    updateUserInfo();
});

// Make all functions globally available
window.isAuthenticated = isAuthenticated;
window.getCurrentUser = getCurrentUser;
window.getUserRole = getUserRole;
window.isAdmin = isAdmin;
window.hasPermission = hasPermission;
window.getAdminModules = getAdminModules;
window.login = login;
window.logout = logout;
window.updateUserInfo = updateUserInfo;
window.requireAuth = requireAuth;
window.requireAdmin = requireAdmin;
window.redirectToDashboard = redirectToDashboard;