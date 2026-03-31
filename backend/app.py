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
from .config import Config
from .database import init_db, close_db

# Import routes - use relative imports
from .routes import (
    library_routes,
    lost_found_routes,
    clubs_routes,
    student_routes,
    medical_routes,
    admin_routes
)

# Create Flask app
# On Vercel, static files are served from the root
app = Flask(__name__,
            static_folder='..',
            static_url_path='',
            template_folder='..')

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
    return send_from_directory('..', 'index.html')

# ==================== API Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'database': 'supabase',
        'timestamp': str(datetime.datetime.now())
    })

# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Resource not found',
        'message': 'The requested URL was not found on the server'
    }), 404

# ==================== Run Application ====================

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
