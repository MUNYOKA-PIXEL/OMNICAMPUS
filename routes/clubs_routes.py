from flask import Blueprint, request, jsonify
from models import Club, ClubEvent
from auth import token_required, admin_required

bp = Blueprint('clubs', __name__)

@bp.route('/', methods=['GET'])
def get_clubs():
    """Get all active clubs"""
    clubs = Club.get_all()
    return jsonify([dict(club) for club in clubs])

@bp.route('/<int:club_id>', methods=['GET'])
def get_club(club_id):
    """Get club by ID"""
    club = Club.get_by_id(club_id)
    if not club:
        return jsonify({'error': 'Club not found'}), 404
    return jsonify(dict(club))

@bp.route('/', methods=['POST'])
@admin_required
def create_club(current_user):
    """Create a new club (admin only)"""
    data = request.json
    
    required_fields = ['name', 'description', 'category', 'contact_email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    club_id = Club.create(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        contact_email=data['contact_email']
    )
    
    return jsonify({'id': club_id, 'message': 'Club created successfully'}), 201

@bp.route('/<int:club_id>/members', methods=['GET'])
@token_required
def get_club_members(current_user, club_id):
    """Get members of a club"""
    members = Club.get_members(club_id)
    return jsonify([dict(member) for member in members])

@bp.route('/<int:club_id>/join', methods=['POST'])
@token_required
def join_club(current_user, club_id):
    """Join a club"""
    Club.add_member(club_id, current_user['id'])
    return jsonify({'message': 'Successfully joined club'})

@bp.route('/<int:club_id>/leave', methods=['POST'])
@token_required
def leave_club(current_user, club_id):
    """Leave a club"""
    Club.remove_member(club_id, current_user['id'])
    return jsonify({'message': 'Successfully left club'})

@bp.route('/<int:club_id>/dues', methods=['POST'])
@token_required
def pay_dues(current_user, club_id):
    """Pay club dues"""
    data = request.json
    amount = data.get('amount', 0)
    
    Club.pay_dues(club_id, current_user['id'], amount)
    return jsonify({'message': 'Dues paid successfully'})

# Events routes
@bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Get all upcoming events"""
    events = ClubEvent.get_upcoming()
    return jsonify([dict(event) for event in events])

@bp.route('/<int:club_id>/events', methods=['GET'])
def get_club_events(club_id):
    """Get events for a specific club"""
    events = ClubEvent.get_by_club(club_id)
    return jsonify([dict(event) for event in events])

@bp.route('/events', methods=['POST'])
@token_required
def create_event(current_user):
    """Create a new club event"""
    data = request.json
    
    required_fields = ['club_id', 'title', 'event_date', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    event_id = ClubEvent.create(
        club_id=data['club_id'],
        title=data['title'],
        description=data.get('description', ''),
        event_date=data['event_date'],
        location=data['location'],
        max_participants=data.get('max_participants', 50),
        created_by=current_user['id']
    )
    
    return jsonify({'id': event_id, 'message': 'Event created successfully'}), 201

@bp.route('/events/<int:event_id>/rsvp', methods=['POST'])
@token_required
def rsvp_event(current_user, event_id):
    """RSVP for an event"""
    rsvp_id = ClubEvent.rsvp(event_id, current_user['id'])
    return jsonify({'id': rsvp_id, 'message': 'RSVP confirmed'})