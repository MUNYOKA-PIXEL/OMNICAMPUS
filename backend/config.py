import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database/omnicampus.db')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    
    # USIU colors for reference
    USIU_BLUE = '#003366'
    USIU_DARK = '#1a1a2e'
    USIU_ACCENT = '#4a90e2'