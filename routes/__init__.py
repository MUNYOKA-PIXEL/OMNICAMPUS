# This file makes the routes directory a Python package
# Export all route modules for easier importing

from . import library_routes
from . import lost_found_routes
from . import clubs_routes
from . import student_routes
from . import medical_routes
from . import admin_routes

__all__ = [
    'library_routes',
    'lost_found_routes',
    'clubs_routes',
    'student_routes',
    'medical_routes',
    'admin_routes'
]