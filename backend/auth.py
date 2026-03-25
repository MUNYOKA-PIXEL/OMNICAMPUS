from functools import wraps
from flask import request, jsonify, session
import jwt
from config import Config
from models import User, Admin

def token_required(f):
    """Decorator to require JWT token for routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Verify token
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            role = payload['role']
            
            # Get user/admin from database
            if role == 'student':
                current_user = User.find_by_id(user_id)
            else:
                current_user = Admin.find_by_username_or_email(str(user_id))
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if hasattr(current_user, 'role') and current_user['role'] in ['admin', 'super_admin']:
            return f(current_user, *args, **kwargs)
        return jsonify({'error': 'Admin access required'}), 403
    
    return decorated