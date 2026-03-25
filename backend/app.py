import sys
import os
import datetime
from pathlib import Path

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Import configuration
from config import Config
from database import init_db, close_db, get_db_connection

# Import routes - use relative imports
from routes import (
    library_routes,
    lost_found_routes,
    clubs_routes,
    student_routes,
    medical_routes,
    admin_routes
)

# Create Flask app
app = Flask(__name__,
            static_folder='../frontend',
            static_url_path='',
            template_folder='../frontend')

# Load configuration
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = Config.JWT_SECRET_KEY
app.config['DEBUG'] = Config.DEBUG

# Enable CORS
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# ==================== Register Blueprints ====================

# Student-facing routes
app.register_blueprint(student_routes.bp)

# Module-specific routes
app.register_blueprint(library_routes.bp, url_prefix='/api/library')
app.register_blueprint(lost_found_routes.bp, url_prefix='/api/lost-found')
app.register_blueprint(clubs_routes.bp, url_prefix='/api/clubs')
app.register_blueprint(medical_routes.bp, url_prefix='/api/medical')

# Admin routes
app.register_blueprint(admin_routes.bp, url_prefix='/api/admin')

# ==================== Database Teardown ====================

@app.teardown_appcontext
def teardown_db(exception):
    """Close database connection at the end of request"""
    close_db(exception)

# ==================== Frontend Routes ====================

@app.route('/')
def serve_index():
    """Serve the main index page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    """Serve any frontend file"""
    frontend_path = os.path.join('../frontend', path)
    if os.path.exists(frontend_path):
        return send_from_directory('../frontend', path)
    
    if '.' not in path:
        return send_from_directory('../frontend', 'index.html')
    
    return jsonify({'error': 'File not found'}), 404

# ==================== API Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        with get_db_connection() as conn:
            conn.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': str(datetime.datetime.now())
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Resource not found',
        'message': 'The requested URL was not found on the server'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    try:
        close_db(error)
    except:
        pass
    
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.errorhandler(403)
def forbidden(error):
    """Handle 403 errors"""
    return jsonify({
        'error': 'Forbidden',
        'message': 'You don\'t have permission to access this resource'
    }), 403

@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 errors"""
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Authentication required'
    }), 401

# ==================== Database Initialization ====================

@app.cli.command('init-db')
def init_db_command():
    """Initialize the database"""
    init_db()
    print('Database initialized.')

# Initialize database on startup if it doesn't exist
with app.app_context():
    db_path = os.path.join(parent_dir, 'database', 'omnicampus.db')
    if not os.path.exists(db_path):
        print("Database not found. Creating new database...")
        init_db()
        print("Database created successfully!")

# ==================== Run Application ====================

if __name__ == '__main__':
    print("=" * 50)
    print("OmniCampus Server Starting...")
    print("=" * 50)
    print(f"Host: {Config.HOST}")
    print(f"Port: {Config.PORT}")
    print(f"Debug Mode: {Config.DEBUG}")
    print(f"Frontend URL: http://{Config.HOST}:{Config.PORT}")
    print(f"API URL: http://{Config.HOST}:{Config.PORT}/api")
    print("=" * 50)
    print("\nAvailable Routes:")
    print("  - Student API: /api/student/*")
    print("  - Library API: /api/library/*")
    print("  - Lost & Found API: /api/lost-found/*")
    print("  - Clubs API: /api/clubs/*")
    print("  - Medical API: /api/medical/*")
    print("  - Admin API: /api/admin/*")
    print("\nFrontend Pages:")
    print("  - Home: /")
    print("  - Login: /login.html")
    print("  - Register: /register.html")
    print("  - Student Dashboard: /dashboard.html")
    print("  - Library: /library.html")
    print("  - Lost & Found: /lost-found.html")
    print("  - Clubs: /clubs.html")
    print("  - Medical: /medical.html")
    print("  - Admin Panel: /admin/index.html")
    print("=" * 50)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG,
        threaded=True
    )