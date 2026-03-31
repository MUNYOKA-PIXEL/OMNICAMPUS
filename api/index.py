import sys
import os

# Add root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app import app as application

# This is the entry point for Vercel
app = application
