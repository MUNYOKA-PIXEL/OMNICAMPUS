from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from backend.models import User, Admin
from backend.auth import token_required, admin_required

bp = Blueprint('medical', __name__, url_prefix='/api/medical')

# ==================== Appointment Routes ====================

@bp.route('/appointments', methods=['GET'])
@token_required
def get_appointments(current_user):
    """Get all appointments for current user"""
    # For demo, return empty array - in real app would query database
    return jsonify([])

@bp.route('/appointments', methods=['POST'])
@token_required
def create_appointment(current_user):
    """Create a new appointment"""
    data = request.json
    
    required_fields = ['service', 'doctor', 'date', 'time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    # In a real app, save to database
    appointment = {
        'id': int(datetime.now().timestamp()),
        'user_id': current_user['id'],
        'service': data['service'],
        'doctor': data['doctor'],
        'date': data['date'],
        'time': data['time'],
        'reason': data.get('reason', ''),
        'status': 'upcoming',
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify(appointment), 201

@bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@token_required
def update_appointment(current_user, appointment_id):
    """Update an appointment"""
    return jsonify({'message': 'Appointment updated successfully'})

@bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@token_required
def cancel_appointment(current_user, appointment_id):
    """Cancel an appointment"""
    return jsonify({'message': 'Appointment cancelled successfully'})

# ==================== Doctor Routes ====================

@bp.route('/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors"""
    doctors = [
        { 
            'id': 1, 
            'name': 'Dr. Sarah Johnson', 
            'specialty': 'General Medicine', 
            'available': True,
            'education': 'MD, Nairobi Medical School',
            'experience': '10 years',
            'languages': ['English', 'Swahili']
        },
        { 
            'id': 2, 
            'name': 'Dr. Michael Chen', 
            'specialty': 'Dentistry', 
            'available': True,
            'education': 'DDS, University of Nairobi',
            'experience': '8 years',
            'languages': ['English', 'Mandarin']
        },
        { 
            'id': 3, 
            'name': 'Dr. Emily Brown', 
            'specialty': 'Counseling', 
            'available': True,
            'education': 'PhD, Clinical Psychology',
            'experience': '12 years',
            'languages': ['English', 'French']
        },
        { 
            'id': 4, 
            'name': 'Dr. James Mwangi', 
            'specialty': 'Eye Care', 
            'available': True,
            'education': 'MBChB, Ophthalmology',
            'experience': '6 years',
            'languages': ['English', 'Swahili', 'Kikuyu']
        }
    ]
    return jsonify(doctors)

@bp.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get doctor by ID"""
    doctors = {
        1: { 
            'id': 1, 
            'name': 'Dr. Sarah Johnson', 
            'specialty': 'General Medicine', 
            'available': True,
            'education': 'MD, Nairobi Medical School',
            'experience': '10 years',
            'languages': ['English', 'Swahili']
        },
        2: { 
            'id': 2, 
            'name': 'Dr. Michael Chen', 
            'specialty': 'Dentistry', 
            'available': True,
            'education': 'DDS, University of Nairobi',
            'experience': '8 years',
            'languages': ['English', 'Mandarin']
        },
        3: { 
            'id': 3, 
            'name': 'Dr. Emily Brown', 
            'specialty': 'Counseling', 
            'available': True,
            'education': 'PhD, Clinical Psychology',
            'experience': '12 years',
            'languages': ['English', 'French']
        },
        4: { 
            'id': 4, 
            'name': 'Dr. James Mwangi', 
            'specialty': 'Eye Care', 
            'available': True,
            'education': 'MBChB, Ophthalmology',
            'experience': '6 years',
            'languages': ['English', 'Swahili', 'Kikuyu']
        }
    }
    
    doctor = doctors.get(doctor_id)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    
    return jsonify(doctor)

# ==================== Medication Routes ====================

@bp.route('/medications', methods=['GET'])
def get_medications():
    """Get all available medications"""
    medications = [
        {'id': 1, 'name': 'Paracetamol 500mg', 'description': 'Pain relief, fever', 'price': 50, 'available': True, 'category': 'Pain Relief'},
        {'id': 2, 'name': 'Amoxicillin 250mg', 'description': 'Antibiotic', 'price': 120, 'available': True, 'category': 'Antibiotics'},
        {'id': 3, 'name': 'Loratadine 10mg', 'description': 'Allergy relief', 'price': 80, 'available': True, 'category': 'Allergy'},
        {'id': 4, 'name': 'Ibuprofen 400mg', 'description': 'Anti-inflammatory', 'price': 65, 'available': False, 'category': 'Pain Relief'},
        {'id': 5, 'name': 'Vitamin C 1000mg', 'description': 'Immune support', 'price': 150, 'available': True, 'category': 'Supplements'}
    ]
    return jsonify(medications)

@bp.route('/medications/<int:medication_id>', methods=['GET'])
def get_medication(medication_id):
    """Get medication by ID"""
    medications = {
        1: {'id': 1, 'name': 'Paracetamol 500mg', 'description': 'Pain relief, fever', 'price': 50, 'available': True},
        2: {'id': 2, 'name': 'Amoxicillin 250mg', 'description': 'Antibiotic', 'price': 120, 'available': True},
        3: {'id': 3, 'name': 'Loratadine 10mg', 'description': 'Allergy relief', 'price': 80, 'available': True},
        4: {'id': 4, 'name': 'Ibuprofen 400mg', 'description': 'Anti-inflammatory', 'price': 65, 'available': False},
        5: {'id': 5, 'name': 'Vitamin C 1000mg', 'description': 'Immune support', 'price': 150, 'available': True}
    }
    
    medication = medications.get(medication_id)
    if not medication:
        return jsonify({'error': 'Medication not found'}), 404
    
    return jsonify(medication)

# ==================== Prescription Routes ====================

@bp.route('/prescriptions', methods=['GET'])
@token_required
def get_prescriptions(current_user):
    """Get prescriptions for current user"""
    # For demo, return sample data
    prescriptions = [
        { 
            'id': 1, 
            'medication': 'Amoxicillin 250mg', 
            'prescribedBy': 'Dr. Sarah Johnson', 
            'date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
            'expires': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
            'refills': 1,
            'instructions': 'Take one capsule twice daily with food',
            'status': 'active'
        },
        { 
            'id': 2, 
            'medication': 'Loratadine 10mg', 
            'prescribedBy': 'Dr. Michael Chen', 
            'date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'expires': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            'refills': 2,
            'instructions': 'Take one tablet daily for allergies',
            'status': 'active'
        }
    ]
    return jsonify(prescriptions)

@bp.route('/prescriptions/<int:prescription_id>/refill', methods=['POST'])
@token_required
def request_refill(current_user, prescription_id):
    """Request prescription refill"""
    return jsonify({'message': 'Refill requested successfully'})

# ==================== Medical Records Routes ====================

@bp.route('/records', methods=['GET'])
@token_required
def get_medical_records(current_user):
    """Get medical records for current user"""
    records = [
        { 
            'id': 1, 
            'date': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
            'type': 'Consultation', 
            'doctor': 'Dr. Emily Brown', 
            'diagnosis': 'Anxiety management', 
            'notes': 'Counseling session - coping strategies discussed'
        },
        { 
            'id': 2, 
            'date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'type': 'Vaccination', 
            'doctor': 'Dr. Sarah Johnson', 
            'diagnosis': 'Preventive care', 
            'notes': 'Annual flu vaccine administered'
        },
        { 
            'id': 3, 
            'date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'type': 'Lab Test', 
            'doctor': 'Dr. Sarah Johnson', 
            'diagnosis': 'Routine checkup', 
            'notes': 'Blood work - all results normal'
        }
    ]
    return jsonify(records)

# ==================== Health Resources Routes ====================

@bp.route('/resources', methods=['GET'])
def get_health_resources():
    """Get health resources"""
    resources = [
        {'id': 1, 'title': 'Mental Health Guide', 'description': 'Resources for stress management and wellness', 'category': 'Mental Health'},
        {'id': 2, 'title': 'First Aid Tips', 'description': 'Basic first aid procedures for common injuries', 'category': 'Emergency'},
        {'id': 3, 'title': 'Nutrition Guide', 'description': 'Healthy eating tips for students', 'category': 'Wellness'},
        {'id': 4, 'title': 'Sexual Health', 'description': 'Confidential information and services', 'category': 'Health'},
        {'id': 5, 'title': 'Sleep Hygiene', 'description': 'Tips for better sleep and rest', 'category': 'Wellness'}
    ]
    return jsonify(resources)

# ==================== Emergency Routes ====================

@bp.route('/emergency', methods=['POST'])
@token_required
def emergency_alert(current_user):
    """Send emergency alert"""
    alert = {
        'user_id': current_user['id'],
        'timestamp': datetime.now().isoformat(),
        'status': 'active'
    }
    # In a real app, this would send SMS/email to security
    return jsonify({'message': 'Emergency alert sent. Help is on the way!'})
