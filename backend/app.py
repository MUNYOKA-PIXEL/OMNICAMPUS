import os
import sys
import datetime
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Add root directory to Python path for imports
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import local modules using absolute package notation
try:
    from backend.config import Config
    from backend.database import close_db
    from routes import (
        library_routes,
        lost_found_routes,
        clubs_routes,
        student_routes,
        medical_routes,
        admin_routes
    )
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback for different environments
    try:
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
    except ImportError:
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

def create_app():
    # root_dir is already defined above
    app = Flask(__name__,
                static_folder=root_dir,
                static_url_path='',
                template_folder=root_dir)

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
        return send_from_directory(root_dir, 'index.html')

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
        full_path = os.path.join(root_dir, path)
        if os.path.exists(full_path) and os.path.isfile(full_path):
            return send_from_directory(root_dir, path)
        
        # Fallback for SPA-like behavior or specific pages
        if '.' not in path:
            return send_from_directory(root_dir, 'index.html')
        
        return jsonify({'error': 'Not found'}), 404
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
