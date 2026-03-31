import os
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
from backend.models import (
    User, LibraryBook, BookLoan, BookRequest,
    LostItem, FoundItem, LostItemClaim, FoundItemClaim,
    Club, ClubEvent, ClubMembership,
    Doctor, Appointment, Medication, Prescription, MedicalRecord,
    Feedback
)
from backend.auth import token_required

bp = Blueprint('student', __name__, url_prefix='/api/student')

# ==================== Authentication Routes ====================

@bp.route('/register', methods=['POST'])
def register():
    """Register a new student"""
    data = request.json
    
    required_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # Check if user already exists
    existing = User.find_by_email_or_id(data['student_id'])
    if existing:
        return jsonify({'error': 'User already exists'}), 400
    
    # Create user
    user_id = User.create(
        student_id=data['student_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password']
    )
    
    # Generate token
    token = User.generate_token(user_id)
    
    return jsonify({
        'id': user_id,
        'token': token,
        'message': 'Registration successful'
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login for students"""
    data = request.json
    
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.authenticate(data['username'], data['password'])
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = User.generate_token(user['id'])
    
    return jsonify({
        'id': user['id'],
        'name': f"{user['first_name']} {user['last_name']}",
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': user['email'],
        'student_id': user['student_id'],
        'phone': user['phone'],
        'token': token,
        'role': 'student'
    })

@bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """Get current user profile"""
    user = User.find_by_id(current_user['id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user['id'],
        'student_id': user['student_id'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'email': user['email'],
        'phone': user['phone'],
        'registration_date': user['registration_date'],
        'role': 'student'
    })

@bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    """Update user profile"""
    data = request.json
    
    updates = {}
    if 'phone' in data:
        updates['phone'] = data['phone']
    if 'email' in data:
        # Check if email is already taken
        existing = User.find_by_email_or_id(data['email'])
        if existing and existing['id'] != current_user['id']:
            return jsonify({'error': 'Email already in use'}), 400
        updates['email'] = data['email']
    
    if updates:
        User.update(current_user['id'], **updates)
    
    return jsonify({'message': 'Profile updated successfully'})

# ==================== Library Routes ====================

@bp.route('/library/books', methods=['GET'])
def get_library_books():
    """Get all library books"""
    books = LibraryBook.get_all()
    return jsonify([dict(book) for book in books])

@bp.route('/library/books/search', methods=['GET'])
def search_library_books():
    """Search books by title, author, or ISBN"""
    query = request.args.get('q', '')
    books = LibraryBook.search(query)
    return jsonify([dict(book) for book in books])

@bp.route('/library/loans', methods=['GET'])
@token_required
def get_my_loans(current_user):
    """Get current user's loans"""
    loans = BookLoan.get_user_loans(current_user['id'])
    return jsonify([dict(loan) for loan in loans])

@bp.route('/library/history', methods=['GET'])
@token_required
def get_loan_history(current_user):
    """Get user's loan history"""
    history = BookLoan.get_user_history(current_user['id'])
    return jsonify([dict(record) for record in history])

@bp.route('/library/requests', methods=['POST'])
@token_required
def request_book(current_user):
    """Request a book"""
    data = request.json
    
    if 'title' not in data:
        return jsonify({'error': 'Book title required'}), 400
    
    request_id = BookRequest.create(
        user_id=current_user['id'],
        book_title=data['title'],
        book_author=data.get('author', '')
    )
    
    return jsonify({
        'id': request_id,
        'message': 'Book request submitted successfully'
    }), 201

@bp.route('/library/requests', methods=['GET'])
@token_required
def get_my_requests(current_user):
    """Get user's book requests"""
    requests = BookRequest.get_user_requests(current_user['id'])
    return jsonify([dict(req) for req in requests])

# ==================== Lost & Found Routes ====================

@bp.route('/lost-found/lost', methods=['POST'])
@token_required
def report_lost_item(current_user):
    """Report a lost item"""
    data = request.json
    
    required_fields = ['item_name', 'description', 'location_lost', 'date_lost']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    item_id = LostItem.create(
        user_id=current_user['id'],
        item_name=data['item_name'],
        description=data['description'],
        category=data.get('category', 'Other'),
        location_lost=data['location_lost'],
        date_lost=data['date_lost']
    )
    
    return jsonify({
        'id': item_id,
        'message': 'Lost item reported successfully'
    }), 201

@bp.route('/lost-found/found', methods=['POST'])
@token_required
def report_found_item(current_user):
    """Report a found item"""
    data = request.json
    
    required_fields = ['item_name', 'description', 'location_found', 'date_found']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    item_id = FoundItem.create(
        user_id=current_user['id'],
        item_name=data['item_name'],
        description=data['description'],
        category=data.get('category', 'Other'),
        location_found=data['location_found'],
        date_found=data['date_found']
    )
    
    return jsonify({
        'id': item_id,
        'message': 'Found item reported successfully'
    }), 201

@bp.route('/lost-found/lost', methods=['GET'])
@token_required
def get_my_lost_items(current_user):
    """Get user's reported lost items"""
    items = LostItem.get_user_items(current_user['id'])
    return jsonify([dict(item) for item in items])

@bp.route('/lost-found/found', methods=['GET'])
@token_required
def get_my_found_items(current_user):
    """Get user's reported found items"""
    items = FoundItem.get_user_items(current_user['id'])
    return jsonify([dict(item) for item in items])

@bp.route('/lost-found/claim/lost/<int:item_id>', methods=['POST'])
@token_required
def claim_lost_item(current_user, item_id):
    """Claim a lost item"""
    claim_id = LostItemClaim.create(item_id, current_user['id'])
    
    return jsonify({
        'id': claim_id,
        'message': 'Claim submitted successfully'
    }), 201

@bp.route('/lost-found/claim/found/<int:item_id>', methods=['POST'])
@token_required
def claim_found_item(current_user, item_id):
    """Claim a found item"""
    claim_id = FoundItemClaim.create(item_id, current_user['id'])
    
    return jsonify({
        'id': claim_id,
        'message': 'Claim submitted successfully'
    }), 201

# ==================== Clubs Routes ====================

@bp.route('/clubs', methods=['GET'])
def get_all_clubs():
    """Get all active clubs"""
    clubs = Club.get_all()
    return jsonify([dict(club) for club in clubs])

@bp.route('/clubs/<int:club_id>', methods=['GET'])
def get_club_details(club_id):
    """Get club details by ID"""
    club = Club.get_by_id(club_id)
    if not club:
        return jsonify({'error': 'Club not found'}), 404
    
    return jsonify(dict(club))

@bp.route('/clubs/<int:club_id>/members', methods=['GET'])
def get_club_members(club_id):
    """Get members of a club"""
    members = Club.get_members(club_id)
    return jsonify([dict(member) for member in members])

@bp.route('/clubs/<int:club_id>/join', methods=['POST'])
@token_required
def join_club(current_user, club_id):
    """Join a club"""
    membership_id = Club.add_member(club_id, current_user['id'])
    
    return jsonify({
        'id': membership_id,
        'message': 'Join request submitted successfully'
    }), 201

@bp.route('/clubs/<int:club_id>/leave', methods=['POST'])
@token_required
def leave_club(current_user, club_id):
    """Leave a club"""
    Club.remove_member(club_id, current_user['id'])
    
    return jsonify({'message': 'Successfully left the club'})

@bp.route('/clubs/<int:club_id>/dues', methods=['POST'])
@token_required
def pay_club_dues(current_user, club_id):
    """Pay club dues"""
    data = request.json
    amount = data.get('amount', 0)
    
    Club.pay_dues(club_id, current_user['id'], amount)
    
    return jsonify({'message': 'Dues paid successfully'})

@bp.route('/clubs/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Get all upcoming events"""
    events = ClubEvent.get_upcoming()
    return jsonify([dict(event) for event in events])

@bp.route('/clubs/<int:club_id>/events', methods=['GET'])
def get_club_events(club_id):
    """Get events for a specific club"""
    events = ClubEvent.get_by_club(club_id)
    return jsonify([dict(event) for event in events])

@bp.route('/clubs/events/<int:event_id>/rsvp', methods=['POST'])
@token_required
def rsvp_to_event(current_user, event_id):
    """RSVP to an event"""
    result = ClubEvent.rsvp(event_id, current_user['id'])
    
    if not result:
        return jsonify({'error': 'Event is full or already RSVP\'d'}), 400
    
    return jsonify({'message': 'RSVP confirmed successfully'})

@bp.route('/clubs/events/<int:event_id>/rsvp', methods=['DELETE'])
@token_required
def cancel_rsvp(current_user, event_id):
    """Cancel RSVP to an event"""
    ClubEvent.cancel_rsvp(event_id, current_user['id'])
    
    return jsonify({'message': 'RSVP cancelled successfully'})

# ==================== Medical Routes ====================

@bp.route('/medical/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    doctors = Doctor.get_all()
    result = []
    for doctor in doctors:
        doctor_dict = dict(doctor)
        if doctor['languages']:
            try:
                doctor_dict['languages'] = json.loads(doctor['languages'])
            except:
                doctor_dict['languages'] = []
        result.append(doctor_dict)
    return jsonify(result)

@bp.route('/medical/doctors/available', methods=['GET'])
def get_available_doctors():
    """Get available doctors"""
    doctors = Doctor.get_available()
    result = []
    for doctor in doctors:
        doctor_dict = dict(doctor)
        if doctor['languages']:
            try:
                doctor_dict['languages'] = json.loads(doctor['languages'])
            except:
                doctor_dict['languages'] = []
        result.append(doctor_dict)
    return jsonify(result)

@bp.route('/medical/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor_details(doctor_id):
    """Get doctor details by ID"""
    doctor = Doctor.get_by_id(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    doctor_dict = dict(doctor)
    if doctor['languages']:
        try:
            doctor_dict['languages'] = json.loads(doctor['languages'])
        except:
            doctor_dict['languages'] = []
    return jsonify(doctor_dict)

@bp.route('/medical/appointments', methods=['POST'])
@token_required
def book_appointment(current_user):
    """Book an appointment"""
    data = request.json
    
    required_fields = ['doctor_id', 'service_type', 'appointment_date', 'appointment_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    appointment_id = Appointment.create(
        user_id=current_user['id'],
        doctor_id=data['doctor_id'],
        service_type=data['service_type'],
        appointment_date=data['appointment_date'],
        appointment_time=data['appointment_time'],
        reason=data.get('reason', ''),
        created_by=current_user['id']
    )
    
    return jsonify({
        'id': appointment_id,
        'message': 'Appointment booked successfully'
    }), 201

@bp.route('/medical/appointments', methods=['GET'])
@token_required
def get_my_appointments(current_user):
    """Get user's appointments"""
    appointments = Appointment.get_user_appointments(current_user['id'])
    return jsonify([dict(apt) for apt in appointments])

@bp.route('/medical/appointments/<int:appointment_id>/cancel', methods=['POST'])
@token_required
def cancel_appointment(current_user, appointment_id):
    """Cancel an appointment"""
    Appointment.cancel(appointment_id, current_user['id'], 'Cancelled by patient')
    
    return jsonify({'message': 'Appointment cancelled successfully'})

@bp.route('/medical/medications', methods=['GET'])
def get_medications():
    """Get all medications"""
    medications = Medication.get_all()
    return jsonify([dict(med) for med in medications])

@bp.route('/medical/medications/available', methods=['GET'])
def get_available_medications():
    """Get available medications"""
    medications = Medication.get_available()
    return jsonify([dict(med) for med in medications])

@bp.route('/medical/prescriptions', methods=['GET'])
@token_required
def get_my_prescriptions(current_user):
    """Get user's prescriptions"""
    prescriptions = Prescription.get_user_prescriptions(current_user['id'])
    return jsonify([dict(pres) for pres in prescriptions])

@bp.route('/medical/prescriptions/<int:prescription_id>/refill', methods=['POST'])
@token_required
def request_refill(current_user, prescription_id):
    """Request prescription refill"""
    refill_id = Prescription.request_refill(prescription_id)
    
    return jsonify({
        'id': refill_id,
        'message': 'Refill request submitted successfully'
    }), 201

@bp.route('/medical/records', methods=['GET'])
@token_required
def get_my_medical_records(current_user):
    """Get user's medical records"""
    records = MedicalRecord.get_user_records(current_user['id'])
    return jsonify([dict(record) for record in records])

# ==================== Feedback Routes ====================

@bp.route('/feedback', methods=['POST'])
@token_required
def submit_feedback(current_user):
    """Submit feedback"""
    data = request.json
    
    if 'message' not in data:
        return jsonify({'error': 'Feedback message required'}), 400
    
    feedback_id = Feedback.create(
        user_id=current_user['id'],
        category=data.get('category', 'General'),
        message=data['message']
    )
    
    return jsonify({
        'id': feedback_id,
        'message': 'Feedback submitted successfully'
    }), 201

# ==================== Dashboard Stats ====================

@bp.route('/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats(current_user):
    """Get dashboard statistics for current user"""
    
    # Get active loans
    active_loans = BookLoan.get_user_loans(current_user['id'])
    
    # Get user's memberships
    memberships = ClubMembership.get_user_memberships(current_user['id'])
    
    # Calculate total fines
    total_fines = sum(loan['fine_amount'] or 0 for loan in active_loans if loan['fine_amount'])
    
    return jsonify({
        'active_loans': len(active_loans),
        'total_fines': total_fines,
        'upcoming_events': 0,  # This would be calculated from events
        'active_clubs': len(memberships)
    })
