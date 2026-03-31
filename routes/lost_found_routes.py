import os
from flask import Blueprint, request, jsonify
from backend.models import LostItem, FoundItem, LostItemClaim, FoundItemClaim
from backend.auth import token_required, admin_required

bp = Blueprint('lost_found', __name__, url_prefix='/api/lost-found')

# Lost items routes
@bp.route('/lost', methods=['GET'])
@admin_required
def get_all_lost(current_user):
    """Get all lost items (admin only)"""
    items = LostItem.get_all()
    return jsonify([dict(item) for item in items])

@bp.route('/lost/user', methods=['GET'])
@token_required
def get_user_lost(current_user):
    """Get lost items for current user"""
    items = LostItem.get_user_items(current_user['id'])
    return jsonify([dict(item) for item in items])

@bp.route('/lost', methods=['POST'])
@token_required
def report_lost(current_user):
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
    
    return jsonify({'id': item_id, 'message': 'Lost item reported successfully'}), 201

@bp.route('/lost/<int:item_id>', methods=['PUT'])
@token_required
def update_lost_item(current_user, item_id):
    """Update lost item status"""
    data = request.json
    
    if 'status' in data:
        LostItem.update_status(item_id, data['status'])
        return jsonify({'message': 'Item status updated'})
    
    return jsonify({'error': 'No update data provided'}), 400

# Found items routes
@bp.route('/found', methods=['GET'])
@admin_required
def get_all_found(current_user):
    """Get all found items (admin only)"""
    items = FoundItem.get_all()
    return jsonify([dict(item) for item in items])

@bp.route('/found/user', methods=['GET'])
@token_required
def get_user_found(current_user):
    """Get found items for current user"""
    items = FoundItem.get_user_items(current_user['id'])
    return jsonify([dict(item) for item in items])

@bp.route('/found', methods=['POST'])
@token_required
def report_found(current_user):
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
    
    return jsonify({'id': item_id, 'message': 'Found item reported successfully'}), 201

@bp.route('/found/<int:item_id>', methods=['PUT'])
@token_required
def update_found_item(current_user, item_id):
    """Update found item status"""
    data = request.json
    
    if 'status' in data:
        FoundItem.update_status(item_id, data['status'])
        return jsonify({'message': 'Item status updated'})
    
    return jsonify({'error': 'No update data provided'}), 400

# Claim routes
@bp.route('/claim/lost/<int:item_id>', methods=['POST'])
@token_required
def claim_lost_item(current_user, item_id):
    """Claim a lost item"""
    claim_id = LostItemClaim.create(item_id, current_user['id'])
    return jsonify({'id': claim_id, 'message': 'Claim submitted successfully'}), 201

@bp.route('/claim/found/<int:item_id>', methods=['POST'])
@token_required
def claim_found_item(current_user, item_id):
    """Claim a found item"""
    claim_id = FoundItemClaim.create(item_id, current_user['id'])
    return jsonify({'id': claim_id, 'message': 'Claim submitted successfully'}), 201

# Match routes
@bp.route('/matches', methods=['GET'])
@admin_required
def find_matches(current_user):
    """Find potential matches between lost and found items"""
    # Simple matching logic
    lost_items = LostItem.get_all()
    found_items = FoundItem.get_all()
    
    matches = []
    for lost in lost_items:
        for found in found_items:
            if (lost['category'] == found['category'] and
                (lost['item_name'].lower() in found['item_name'].lower() or
                 found['item_name'].lower() in lost['item_name'].lower())):
                matches.append({
                    'lost_item': dict(lost),
                    'found_item': dict(found),
                    'score': 0.8
                })
    
    return jsonify(matches)
