import sys
import os
from pathlib import Path

# Get the absolute path to the project root
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent  # Goes up two levels: routes/ -> backend/ -> project root
sys.path.insert(0, str(project_root))

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
from backend.models import (
    User, Admin, LibraryAdmin, LostFoundAdmin, ClubsAdmin, MedicalAdmin, UserAdmin,
    LibraryBook, BookLoan, BookRequest,
    LostItem, FoundItem, LostItemClaim, FoundItemClaim,
    Club, ClubEvent, ClubMembership,
    Doctor, Appointment, Medication, Prescription, MedicalRecord,
    Feedback
)
from backend.auth import token_required, admin_required

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ==================== Authentication Routes ====================

@bp.route('/login', methods=['POST'])
def admin_login():
    """Login for all admin types"""
    data = request.json
    
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    
    # Try each admin type in order
    admin = None
    role = None
    token = None
    admin_type = None
    admin_id = None
    full_name = None
    email = None
    permissions = []
    
    # Try super admin
    admin = Admin.authenticate(username, password)
    if admin:
        role = 'super_admin'
        token = Admin.generate_token(admin['id'])
        admin_type = 'super_admin'
        admin_id = admin['id']
        full_name = admin['full_name']
        email = admin['email']
        permissions = ['all']
    else:
        # Try library admin
        admin = LibraryAdmin.authenticate(username, password)
        if admin:
            role = 'library_admin'
            token = LibraryAdmin.generate_token(admin['id'])
            admin_type = 'library_admin'
            admin_id = admin['id']
            full_name = admin['full_name']
            email = admin['email']
            
            # Build permissions
            if admin['can_add_books']: permissions.append('add_books')
            if admin['can_edit_books']: permissions.append('edit_books')
            if admin['can_delete_books']: permissions.append('delete_books')
            if admin['can_manage_loans']: permissions.append('manage_loans')
            if admin['can_approve_requests']: permissions.append('approve_requests')
        else:
            # Try lost & found admin
            admin = LostFoundAdmin.authenticate(username, password)
            if admin:
                role = 'lost_found_admin'
                token = LostFoundAdmin.generate_token(admin['id'])
                admin_type = 'lost_found_admin'
                admin_id = admin['id']
                full_name = admin['full_name']
                email = admin['email']
                
                # Build permissions
                if admin['can_verify_items']: permissions.append('verify_items')
                if admin['can_approve_claims']: permissions.append('approve_claims')
                if admin['can_delete_items']: permissions.append('delete_items')
                if admin['can_manage_matches']: permissions.append('manage_matches')
            else:
                # Try clubs admin
                admin = ClubsAdmin.authenticate(username, password)
                if admin:
                    role = 'clubs_admin'
                    token = ClubsAdmin.generate_token(admin['id'])
                    admin_type = 'clubs_admin'
                    admin_id = admin['id']
                    full_name = admin['full_name']
                    email = admin['email']
                    
                    # Build permissions
                    if admin['can_create_clubs']: permissions.append('create_clubs')
                    if admin['can_edit_clubs']: permissions.append('edit_clubs')
                    if admin['can_delete_clubs']: permissions.append('delete_clubs')
                    if admin['can_approve_members']: permissions.append('approve_members')
                    if admin['can_manage_events']: permissions.append('manage_events')
                else:
                    # Try medical admin
                    admin = MedicalAdmin.authenticate(username, password)
                    if admin:
                        role = 'medical_admin'
                        token = MedicalAdmin.generate_token(admin['id'])
                        admin_type = 'medical_admin'
                        admin_id = admin['id']
                        full_name = admin['full_name']
                        email = admin['email']
                        
                        # Build permissions
                        if admin['can_manage_doctors']: permissions.append('manage_doctors')
                        if admin['can_manage_appointments']: permissions.append('manage_appointments')
                        if admin['can_manage_prescriptions']: permissions.append('manage_prescriptions')
                        if admin['can_manage_records']: permissions.append('manage_records')
                        if admin['can_manage_medications']: permissions.append('manage_medications')
                    else:
                        # Try user admin
                        admin = UserAdmin.authenticate(username, password)
                        if admin:
                            role = 'user_admin'
                            token = UserAdmin.generate_token(admin['id'])
                            admin_type = 'user_admin'
                            admin_id = admin['id']
                            full_name = admin['full_name']
                            email = admin['email']
                            
                            # Build permissions
                            if admin['can_view_users']: permissions.append('view_users')
                            if admin['can_edit_users']: permissions.append('edit_users')
                            if admin['can_delete_users']: permissions.append('delete_users')
    
    if not admin:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return jsonify({
        'id': admin_id,
        'name': full_name,
        'username': username,
        'email': email,
        'role': role,
        'admin_type': admin_type,
        'permissions': permissions,
        'token': token
    })

# ==================== Dashboard Routes ====================

@bp.route('/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats(current_admin):
    """Get dashboard statistics based on admin role"""
    
    stats = {}
    
    if current_admin['role'] == 'super_admin' or current_admin['role'] == 'library_admin':
        books = LibraryBook.get_all()
        stats['total_books'] = len(books) if books else 0
        
        loans = BookLoan.get_current_loans()
        stats['active_loans'] = len(loans) if loans else 0
        
        requests = BookRequest.get_pending()
        stats['pending_requests'] = len(requests) if requests else 0
    
    if current_admin['role'] == 'super_admin' or current_admin['role'] == 'lost_found_admin':
        lost = LostItem.get_all()
        stats['lost_items'] = len(lost) if lost else 0
        
        found = FoundItem.get_all()
        stats['found_items'] = len(found) if found else 0
        
        lost_claims = LostItemClaim.get_pending()
        found_claims = FoundItemClaim.get_pending()
        stats['pending_claims'] = (len(lost_claims) if lost_claims else 0) + (len(found_claims) if found_claims else 0)
    
    if current_admin['role'] == 'super_admin' or current_admin['role'] == 'clubs_admin':
        clubs = Club.get_all()
        stats['total_clubs'] = len(clubs) if clubs else 0
        
        pending_clubs = Club.get_pending()
        stats['pending_clubs'] = len(pending_clubs) if pending_clubs else 0
        
        events = ClubEvent.get_upcoming()
        stats['upcoming_events'] = len(events) if events else 0
    
    if current_admin['role'] == 'super_admin' or current_admin['role'] == 'medical_admin':
        doctors = Doctor.get_all()
        stats['total_doctors'] = len(doctors) if doctors else 0
        
        appointments = Appointment.get_upcoming()
        today = datetime.now().strftime('%Y-%m-%d')
        stats['today_appointments'] = len([a for a in appointments if a['appointment_date'] == today]) if appointments else 0
        
        stats['pending_refills'] = 0  # Would query prescription_refills
    
    if current_admin['role'] == 'super_admin' or current_admin['role'] == 'user_admin':
        users = User.get_all()
        stats['total_users'] = len(users) if users else 0
        
        feedback = Feedback.get_new()
        stats['new_feedback'] = len(feedback) if feedback else 0
    
    return jsonify(stats)

# ==================== Library Admin Routes ====================

@bp.route('/library/books', methods=['GET'])
@admin_required
def get_all_books(current_admin):
    """Get all library books"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    books = LibraryBook.get_all()
    return jsonify([dict(book) for book in books]) if books else jsonify([])

@bp.route('/library/books', methods=['POST'])
@admin_required
def add_book(current_admin):
    """Add a new book"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    required_fields = ['title', 'author', 'total_copies']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    book_id = LibraryBook.create(
        title=data['title'],
        author=data['author'],
        isbn=data.get('isbn', ''),
        category=data.get('category', 'General'),
        total_copies=data['total_copies'],
        added_by=current_admin['id'] if current_admin['role'] == 'library_admin' else None
    )
    
    return jsonify({
        'id': book_id,
        'message': 'Book added successfully'
    }), 201

@bp.route('/library/books/<int:book_id>', methods=['PUT'])
@admin_required
def update_book(current_admin, book_id):
    """Update book details"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    LibraryBook.update(book_id, **data)
    return jsonify({'message': 'Book updated successfully'})

@bp.route('/library/books/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_book(current_admin, book_id):
    """Delete a book"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    LibraryBook.delete(book_id)
    return jsonify({'message': 'Book deleted successfully'})

@bp.route('/library/loans', methods=['GET'])
@admin_required
def get_all_loans(current_admin):
    """Get all current loans"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    loans = BookLoan.get_current_loans()
    return jsonify([dict(loan) for loan in loans]) if loans else jsonify([])

@bp.route('/library/loans', methods=['POST'])
@admin_required
def issue_book(current_admin):
    """Issue a book to a student"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    required_fields = ['user_id', 'book_id', 'due_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    loan_id = BookLoan.issue_book(
        user_id=data['user_id'],
        book_id=data['book_id'],
        due_date=data['due_date'],
        issued_by=current_admin['id'] if current_admin['role'] == 'library_admin' else None
    )
    
    if not loan_id:
        return jsonify({'error': 'Book not available'}), 400
    
    return jsonify({
        'id': loan_id,
        'message': 'Book issued successfully'
    }), 201

@bp.route('/library/loans/<int:loan_id>/return', methods=['POST'])
@admin_required
def return_book(current_admin, loan_id):
    """Return a book"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    success = BookLoan.return_book(loan_id, current_admin['id'] if current_admin['role'] == 'library_admin' else None)
    
    if not success:
        return jsonify({'error': 'Loan not found or already returned'}), 400
    
    return jsonify({'message': 'Book returned successfully'})

@bp.route('/library/requests', methods=['GET'])
@admin_required
def get_pending_requests(current_admin):
    """Get pending book requests"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    requests = BookRequest.get_pending()
    return jsonify([dict(req) for req in requests]) if requests else jsonify([])

@bp.route('/library/requests/<int:request_id>/approve', methods=['POST'])
@admin_required
def approve_book_request(current_admin, request_id):
    """Approve a book request"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    BookRequest.approve(request_id, current_admin['id'] if current_admin['role'] == 'library_admin' else None)
    return jsonify({'message': 'Request approved successfully'})

@bp.route('/library/requests/<int:request_id>/reject', methods=['POST'])
@admin_required
def reject_book_request(current_admin, request_id):
    """Reject a book request"""
    if current_admin['role'] not in ['super_admin', 'library_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    notes = data.get('notes', '')
    BookRequest.reject(request_id, current_admin['id'] if current_admin['role'] == 'library_admin' else None, notes)
    return jsonify({'message': 'Request rejected successfully'})

# ==================== Lost & Found Admin Routes ====================

@bp.route('/lost-found/lost', methods=['GET'])
@admin_required
def get_all_lost_items(current_admin):
    """Get all lost items"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    items = LostItem.get_all()
    return jsonify([dict(item) for item in items]) if items else jsonify([])

@bp.route('/lost-found/found', methods=['GET'])
@admin_required
def get_all_found_items(current_admin):
    """Get all found items"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    items = FoundItem.get_all()
    return jsonify([dict(item) for item in items]) if items else jsonify([])

@bp.route('/lost-found/lost/<int:item_id>/verify', methods=['POST'])
@admin_required
def verify_lost_item(current_admin, item_id):
    """Verify a lost item"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    LostItem.verify(item_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None)
    return jsonify({'message': 'Item verified successfully'})

@bp.route('/lost-found/found/<int:item_id>/verify', methods=['POST'])
@admin_required
def verify_found_item(current_admin, item_id):
    """Verify a found item"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    FoundItem.verify(item_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None)
    return jsonify({'message': 'Item verified successfully'})

@bp.route('/lost-found/found/<int:item_id>/return', methods=['POST'])
@admin_required
def mark_found_item_returned(current_admin, item_id):
    """Mark a found item as returned"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    FoundItem.mark_returned(item_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None)
    return jsonify({'message': 'Item marked as returned'})

@bp.route('/lost-found/claims/lost', methods=['GET'])
@admin_required
def get_pending_lost_claims(current_admin):
    """Get pending lost item claims"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    claims = LostItemClaim.get_pending()
    return jsonify([dict(claim) for claim in claims]) if claims else jsonify([])

@bp.route('/lost-found/claims/found', methods=['GET'])
@admin_required
def get_pending_found_claims(current_admin):
    """Get pending found item claims"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    claims = FoundItemClaim.get_pending()
    return jsonify([dict(claim) for claim in claims]) if claims else jsonify([])

@bp.route('/lost-found/claims/lost/<int:claim_id>/approve', methods=['POST'])
@admin_required
def approve_lost_claim(current_admin, claim_id):
    """Approve a lost item claim"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    LostItemClaim.approve(claim_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None)
    return jsonify({'message': 'Claim approved successfully'})

@bp.route('/lost-found/claims/lost/<int:claim_id>/reject', methods=['POST'])
@admin_required
def reject_lost_claim(current_admin, claim_id):
    """Reject a lost item claim"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    notes = data.get('notes', '')
    LostItemClaim.reject(claim_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None, notes)
    return jsonify({'message': 'Claim rejected'})

@bp.route('/lost-found/claims/found/<int:claim_id>/approve', methods=['POST'])
@admin_required
def approve_found_claim(current_admin, claim_id):
    """Approve a found item claim"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    FoundItemClaim.approve(claim_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None)
    return jsonify({'message': 'Claim approved successfully'})

@bp.route('/lost-found/claims/found/<int:claim_id>/reject', methods=['POST'])
@admin_required
def reject_found_claim(current_admin, claim_id):
    """Reject a found item claim"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    notes = data.get('notes', '')
    FoundItemClaim.reject(claim_id, current_admin['id'] if current_admin['role'] == 'lost_found_admin' else None, notes)
    return jsonify({'message': 'Claim rejected'})

@bp.route('/lost-found/items/lost/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_lost_item(current_admin, item_id):
    """Delete a lost item"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    LostItem.delete(item_id)
    return jsonify({'message': 'Item deleted successfully'})

@bp.route('/lost-found/items/found/<int:item_id>', methods=['DELETE'])
@admin_required
def delete_found_item(current_admin, item_id):
    """Delete a found item"""
    if current_admin['role'] not in ['super_admin', 'lost_found_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    FoundItem.delete(item_id)
    return jsonify({'message': 'Item deleted successfully'})

# ==================== Clubs Admin Routes ====================

@bp.route('/clubs', methods=['GET'])
@admin_required
def get_all_clubs_admin(current_admin):
    """Get all clubs (including pending)"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    clubs = Club.get_all()
    return jsonify([dict(club) for club in clubs]) if clubs else jsonify([])

@bp.route('/clubs/pending', methods=['GET'])
@admin_required
def get_pending_clubs(current_admin):
    """Get pending club approvals"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    clubs = Club.get_pending()
    return jsonify([dict(club) for club in clubs]) if clubs else jsonify([])

@bp.route('/clubs', methods=['POST'])
@admin_required
def create_club(current_admin):
    """Create a new club"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    required_fields = ['name', 'description', 'category', 'contact_email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    club_id = Club.create(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        contact_email=data['contact_email'],
        dues_amount=data.get('dues_amount', 0),
        created_by=current_admin['id'] if current_admin['role'] == 'clubs_admin' else None
    )
    
    return jsonify({
        'id': club_id,
        'message': 'Club created successfully'
    }), 201

@bp.route('/clubs/<int:club_id>/approve', methods=['POST'])
@admin_required
def approve_club(current_admin, club_id):
    """Approve a club"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    Club.approve(club_id, current_admin['id'] if current_admin['role'] == 'clubs_admin' else None)
    return jsonify({'message': 'Club approved successfully'})

@bp.route('/clubs/<int:club_id>', methods=['PUT'])
@admin_required
def update_club(current_admin, club_id):
    """Update club details"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    Club.update(club_id, **data)
    return jsonify({'message': 'Club updated successfully'})

@bp.route('/clubs/<int:club_id>', methods=['DELETE'])
@admin_required
def delete_club(current_admin, club_id):
    """Delete a club"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    Club.delete(club_id)
    return jsonify({'message': 'Club deleted successfully'})

@bp.route('/clubs/memberships/pending', methods=['GET'])
@admin_required
def get_pending_memberships(current_admin):
    """Get pending club membership requests"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    memberships = ClubMembership.get_pending_requests()
    return jsonify([dict(m) for m in memberships]) if memberships else jsonify([])

@bp.route('/clubs/memberships/<int:membership_id>/approve', methods=['POST'])
@admin_required
def approve_membership(current_admin, membership_id):
    """Approve a club membership request"""
    if current_admin['role'] not in ['super_admin', 'clubs_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    Club.approve_member(membership_id, current_admin['id'] if current_admin['role'] == 'clubs_admin' else None)
    return jsonify({'message': 'Membership approved successfully'})

# ==================== Medical Admin Routes ====================

@bp.route('/medical/doctors', methods=['GET'])
@admin_required
def get_all_doctors(current_admin):
    """Get all doctors"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    doctors = Doctor.get_all()
    result = []
    if doctors:
        for doctor in doctors:
            doctor_dict = dict(doctor)
            if doctor['languages']:
                try:
                    doctor_dict['languages'] = json.loads(doctor['languages'])
                except:
                    doctor_dict['languages'] = []
            result.append(doctor_dict)
    return jsonify(result)

@bp.route('/medical/doctors', methods=['POST'])
@admin_required
def add_doctor(current_admin):
    """Add a new doctor"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    required_fields = ['name', 'specialty', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    doctor_id = Doctor.create(
        name=data['name'],
        specialty=data['specialty'],
        email=data['email'],
        phone=data.get('phone', ''),
        education=data.get('education', ''),
        experience=data.get('experience', ''),
        languages=data.get('languages', []),
        created_by=current_admin['id'] if current_admin['role'] == 'medical_admin' else None
    )
    
    return jsonify({
        'id': doctor_id,
        'message': 'Doctor added successfully'
    }), 201

@bp.route('/medical/doctors/<int:doctor_id>', methods=['PUT'])
@admin_required
def update_doctor(current_admin, doctor_id):
    """Update doctor details"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    Doctor.update(doctor_id, **data)
    return jsonify({'message': 'Doctor updated successfully'})

@bp.route('/medical/doctors/<int:doctor_id>/toggle', methods=['POST'])
@admin_required
def toggle_doctor_availability(current_admin, doctor_id):
    """Toggle doctor availability"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    new_status = Doctor.toggle_availability(doctor_id)
    status_text = 'available' if new_status else 'unavailable'
    return jsonify({'message': f'Doctor is now {status_text}'})

@bp.route('/medical/appointments', methods=['GET'])
@admin_required
def get_all_appointments(current_admin):
    """Get all appointments"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    appointments = Appointment.get_upcoming()
    return jsonify([dict(apt) for apt in appointments]) if appointments else jsonify([])

@bp.route('/medical/appointments/<int:appointment_id>/confirm', methods=['POST'])
@admin_required
def confirm_appointment(current_admin, appointment_id):
    """Confirm an appointment"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    Appointment.confirm(appointment_id, current_admin['id'] if current_admin['role'] == 'medical_admin' else None)
    return jsonify({'message': 'Appointment confirmed'})

@bp.route('/medical/appointments/<int:appointment_id>/cancel', methods=['POST'])
@admin_required
def cancel_appointment_admin(current_admin, appointment_id):
    """Cancel an appointment"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    reason = data.get('reason', 'Cancelled by admin')
    Appointment.cancel(appointment_id, current_admin['id'] if current_admin['role'] == 'medical_admin' else None, reason)
    return jsonify({'message': 'Appointment cancelled'})

@bp.route('/medical/appointments/<int:appointment_id>/complete', methods=['POST'])
@admin_required
def complete_appointment(current_admin, appointment_id):
    """Mark appointment as completed"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    Appointment.complete(appointment_id)
    return jsonify({'message': 'Appointment marked as completed'})

@bp.route('/medical/medications', methods=['GET'])
@admin_required
def get_all_medications(current_admin):
    """Get all medications"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    medications = Medication.get_all()
    return jsonify([dict(med) for med in medications]) if medications else jsonify([])

@bp.route('/medical/medications', methods=['POST'])
@admin_required
def add_medication(current_admin):
    """Add a new medication"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    
    required_fields = ['name', 'price', 'stock']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    medication_id = Medication.create(
        name=data['name'],
        description=data.get('description', ''),
        category=data.get('category', 'General'),
        price=data['price'],
        stock=data['stock'],
        requires_prescription=data.get('requires_prescription', True),
        created_by=current_admin['id'] if current_admin['role'] == 'medical_admin' else None
    )
    
    return jsonify({
        'id': medication_id,
        'message': 'Medication added successfully'
    }), 201

@bp.route('/medical/medications/<int:medication_id>', methods=['PUT'])
@admin_required
def update_medication(current_admin, medication_id):
    """Update medication details"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    Medication.update(medication_id, **data)
    return jsonify({'message': 'Medication updated successfully'})

@bp.route('/medical/medications/<int:medication_id>/stock', methods=['POST'])
@admin_required
def update_medication_stock(current_admin, medication_id):
    """Update medication stock"""
    if current_admin['role'] not in ['super_admin', 'medical_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    quantity = data.get('quantity', 0)
    Medication.update_stock(medication_id, quantity)
    return jsonify({'message': 'Stock updated successfully'})

# ==================== User Admin Routes ====================

@bp.route('/users', methods=['GET'])
@admin_required
def get_all_users(current_admin):
    """Get all users"""
    if current_admin['role'] not in ['super_admin', 'user_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.get_all()
    # Remove password hashes from response
    result = []
    if users:
        for user in users:
            user_dict = dict(user)
            user_dict.pop('password_hash', None)
            result.append(user_dict)
    return jsonify(result)

@bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_details(current_admin, user_id):
    """Get user details by ID"""
    if current_admin['role'] not in ['super_admin', 'user_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_dict = dict(user)
    user_dict.pop('password_hash', None)
    return jsonify(user_dict)

@bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(current_admin, user_id):
    """Update user details"""
    if current_admin['role'] not in ['super_admin', 'user_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    updates = {}
    
    if 'first_name' in data:
        updates['first_name'] = data['first_name']
    if 'last_name' in data:
        updates['last_name'] = data['last_name']
    if 'email' in data:
        # Check if email is already taken
        existing = User.find_by_email_or_id(data['email'])
        if existing and existing['id'] != user_id:
            return jsonify({'error': 'Email already in use'}), 400
        updates['email'] = data['email']
    if 'phone' in data:
        updates['phone'] = data['phone']
    if 'is_active' in data:
        updates['is_active'] = data['is_active']
    
    if updates:
        User.update(user_id, **updates)
    
    return jsonify({'message': 'User updated successfully'})

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_admin, user_id):
    """Soft delete a user"""
    if current_admin['role'] not in ['super_admin', 'user_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    User.delete(user_id)
    return jsonify({'message': 'User deactivated successfully'})

# ==================== Feedback Routes ====================

@bp.route('/feedback', methods=['GET'])
@admin_required
def get_all_feedback(current_admin):
    """Get all feedback"""
    feedback = Feedback.get_all()
    return jsonify([dict(f) for f in feedback]) if feedback else jsonify([])

@bp.route('/feedback/new', methods=['GET'])
@admin_required
def get_new_feedback(current_admin):
    """Get new feedback"""
    feedback = Feedback.get_new()
    return jsonify([dict(f) for f in feedback]) if feedback else jsonify([])

@bp.route('/feedback/<int:feedback_id>/respond', methods=['POST'])
@admin_required
def respond_to_feedback(current_admin, feedback_id):
    """Respond to feedback"""
    data = request.json
    
    if 'response' not in data:
        return jsonify({'error': 'Response message required'}), 400
    
    Feedback.respond(feedback_id, current_admin['id'] if current_admin['role'] != 'super_admin' else None, data['response'])
    
    return jsonify({'message': 'Response sent successfully'})
