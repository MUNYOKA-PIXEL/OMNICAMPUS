import os
from dotenv import load_dotenv

# Load environment variables if .env exists (local development)
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'omnicampus-secret-key-12345')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres.qhehkycouyytrhcexngx:Sunch.1%40P8519@aws-0-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require')
    SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://qhehkycouyytrhcexngx.supabase.co')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFoZWhreWNvdXl5dHJoY2V4bmd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ5NjAwOTAsImV4cCI6MjA5MDUzNjA5MH0.RNfMw2TNErRe7OQwP_uRHel7-R-bZWSAJjof5ndDP6k')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'omnicampus-jwt-secret-key-12345')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # USIU colors for reference
    USIU_BLUE = '#003366'
    USIU_DARK = '#1a1a2e'
    USIU_ACCENT = '#4a90e2'
