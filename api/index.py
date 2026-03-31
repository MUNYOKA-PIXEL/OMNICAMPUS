import sys
import os
import traceback

# Add the root directory to the path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.insert(0, path)

try:
    from backend.app import app
except Exception as e:
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/api/<path:path>')
    def catch_all(path):
        error_info = {
            "error": "Failed to import application",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "sys_path": sys.path,
            "cwd": os.getcwd()
        }
        return jsonify(error_info), 500
    
    @app.route('/')
    def root_error():
        return f"<h1>Backend Import Error</h1><pre>{traceback.format_exc()}</pre>", 500
