import sys
import os
import datetime
from pathlib import Path

# Add the current directory and its parent to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Import local modules - use absolute imports since we've added paths
try:
    from config import Config
    from database import close_db
    from routes import (
        library_routes,
        lost_found_routes,
        clubs_routes,
        student_routes,
        medical_routes,
        admin_routes
    )
except ImportError:
    from .config import Config
    from .database import close_db
    from .routes import (
        library_routes,
        lost_found_routes,
        clubs_routes,
        student_routes,
        medical_routes,
        admin_routes
    )

# Create Flask app
# On Vercel, static files are now in the root of the project
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
app.register_blueprint(student_routes.bp)
app.register_blueprint(library_routes.bp, url_prefix='/api/library')
app.register_blueprint(lost_found_routes.bp, url_prefix='/api/lost-found')
app.register_blueprint(clubs_routes.bp, url_prefix='/api/clubs')
app.register_blueprint(medical_routes.bp, url_prefix='/api/medical')
app.register_blueprint(admin_routes.bp, url_prefix='/api/admin')

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# ==================== Frontend & Health Routes ====================

@app.route('/')
def serve_index():
    return send_from_directory('..', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'database': 'supabase',
        'timestamp': str(datetime.datetime.now())
    })

# If someone visits a frontend route that isn't handled by static files
@app.route('/<path:path>')
def serve_any_path(path):
    # If the path exists in the root, serve it
    if os.path.exists(os.path.join(parent_dir, path)):
        return send_from_directory('..', path)
    
    # Fallback for SPA-like behavior or specific pages
    if '.' not in path:
        return send_from_directory('..', 'index.html')
    
    return jsonify({'error': 'Not found'}), 404

# ==================== Run Application ====================
if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
