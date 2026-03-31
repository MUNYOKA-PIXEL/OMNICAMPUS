import datetime
import jwt
import bcrypt
from .database import get_db, execute_db, query_db
from .config import Config

# Initialize the Supabase client
supabase = get_db()

# ==================== User Models ====================

class User:
    """User/Student model"""
    
    @staticmethod
    def create(data):
        if 'password' in data:
            password = data.pop('password')
            data['password_hash'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        return execute_db('users', data, operation='insert')
    
    @staticmethod
    def find_by_student_id(student_id):
        return query_db('users', filters={'student_id': student_id}, one=True)
    
    @staticmethod
    def find_by_email(email):
        return query_db('users', filters={'email': email}, one=True)
    
    @staticmethod
    def find_by_id(user_id):
        return query_db('users', filters={'id': user_id}, one=True)
    
    @staticmethod
    def find_by_email_or_id(value):
        user = query_db('users', filters={'email': value}, one=True)
        if not user:
            user = query_db('users', filters={'student_id': value}, one=True)
        return user

    @staticmethod
    def get_all():
        return query_db('users')

    @staticmethod
    def authenticate(username_or_email, password):
        user = User.find_by_email_or_id(username_or_email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
        return None

    @staticmethod
    def generate_token(user_id):
        payload = {
            'user_id': user_id,
            'role': 'student',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

class AdminBase:
    @classmethod
    def find_by_username(cls, table, username):
        return query_db(table, filters={'username': username}, one=True)
    
    @classmethod
    def find_by_email(cls, table, email):
        return query_db(table, filters={'email': email}, one=True)
    
    @classmethod
    def find_by_username_or_email(cls, table, value):
        admin = query_db(table, filters={'username': value}, one=True)
        if not admin:
            admin = query_db(table, filters={'email': value}, one=True)
        return admin

    @classmethod
    def authenticate(cls, table, username, password):
        admin = cls.find_by_username_or_email(table, username)
        # For simplicity in this campus system, we might have plain text or hashed
        # Check if password matches (handling both for flexibility)
        if admin:
            if 'password_hash' in admin:
                if bcrypt.checkpw(password.encode('utf-8'), admin['password_hash'].encode('utf-8')):
                    return admin
            elif admin.get('password') == password:
                return admin
        return None

    @classmethod
    def generate_token(cls, admin_id, role):
        payload = {
            'user_id': admin_id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

class Admin(AdminBase):
    """Super Admin model"""
    @staticmethod
    def find_by_username_or_email(value): return AdminBase.find_by_username_or_email('admins', value)
    @staticmethod
    def authenticate(username, password): return AdminBase.authenticate('admins', username, password)
    @staticmethod
    def generate_token(admin_id): return AdminBase.generate_token(admin_id, 'super_admin')
    @staticmethod
    def get_all(): return query_db('admins')

class LibraryAdmin(AdminBase):
    @staticmethod
    def authenticate(username, password): return AdminBase.authenticate('library_admins', username, password)
    @staticmethod
    def generate_token(admin_id): return AdminBase.generate_token(admin_id, 'library_admin')
    @staticmethod
    def get_all(): return query_db('library_admins')

class LostFoundAdmin(AdminBase):
    @staticmethod
    def authenticate(username, password): return AdminBase.authenticate('lost_found_admins', username, password)
    @staticmethod
    def generate_token(admin_id): return AdminBase.generate_token(admin_id, 'lost_found_admin')
    @staticmethod
    def get_all(): return query_db('lost_found_admins')

class ClubsAdmin(AdminBase):
    @staticmethod
    def authenticate(username, password): return AdminBase.authenticate('clubs_admins', username, password)
    @staticmethod
    def generate_token(admin_id): return AdminBase.generate_token(admin_id, 'clubs_admin')
    @staticmethod
    def get_all(): return query_db('clubs_admins')

class MedicalAdmin(AdminBase):
    @staticmethod
    def authenticate(username, password): return AdminBase.authenticate('medical_admins', username, password)
    @staticmethod
    def generate_token(admin_id): return AdminBase.generate_token(admin_id, 'medical_admin')
    @staticmethod
    def get_all(): return query_db('medical_admins')

class UserAdmin(AdminBase):
    @staticmethod
    def authenticate(username, password): return AdminBase.authenticate('user_admins', username, password)
    @staticmethod
    def generate_token(admin_id): return AdminBase.generate_token(admin_id, 'user_admin')
    @staticmethod
    def get_all(): return query_db('user_admins')

# ==================== Library Models ====================

class LibraryBook:
    @staticmethod
    def get_all(): return query_db('books')
    @staticmethod
    def find_by_id(book_id): return query_db('books', filters={'id': book_id}, one=True)
    @staticmethod
    def create(data): return execute_db('books', data, operation='insert')
    @staticmethod
    def update(book_id, **kwargs): return execute_db('books', kwargs, operation='update', filters={'id': book_id})
    @staticmethod
    def delete(book_id): return execute_db('books', {}, operation='delete', filters={'id': book_id})

class BookLoan:
    @staticmethod
    def get_all(): return query_db('loans')
    @staticmethod
    def get_current_loans(): return query_db('loans', filters={'status': 'issued'})
    @staticmethod
    def get_by_user(user_id): return query_db('loans', filters={'user_id': user_id})

class BookRequest:
    @staticmethod
    def get_all(): return query_db('book_requests')
    @staticmethod
    def get_pending(): return query_db('book_requests', filters={'status': 'pending'})

# ==================== Lost & Found Models ====================

class LostItem:
    @staticmethod
    def get_all(): return query_db('lost_items')

class FoundItem:
    @staticmethod
    def get_all(): return query_db('found_items')

class LostItemClaim:
    @staticmethod
    def get_pending(): return query_db('lost_item_claims', filters={'status': 'pending'})

class FoundItemClaim:
    @staticmethod
    def get_pending(): return query_db('found_item_claims', filters={'status': 'pending'})

# ==================== Club Models ====================

class Club:
    @staticmethod
    def get_all(): return query_db('clubs')
    @staticmethod
    def get_pending(): return query_db('clubs', filters={'status': 'pending'})

class ClubEvent:
    @staticmethod
    def get_all(): return query_db('club_events')
    @staticmethod
    def get_upcoming():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return supabase.table('club_events').select('*').gte('event_date', today).execute().data

class ClubMembership:
    @staticmethod
    def get_by_user(user_id): return query_db('club_memberships', filters={'user_id': user_id})
    @staticmethod
    def get_pending_requests(): return query_db('club_memberships', filters={'status': 'pending'})

# ==================== Medical Models ====================

class Doctor:
    @staticmethod
    def get_all(): return query_db('doctors')

class Appointment:
    @staticmethod
    def get_all(): return query_db('appointments')
    @staticmethod
    def get_upcoming():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return supabase.table('appointments').select('*').gte('appointment_date', today).execute().data

class Medication:
    @staticmethod
    def get_all(): return query_db('medications')

# ==================== Feedback Model ====================

class Feedback:
    @staticmethod
    def get_all():
        result = supabase.table('feedback').select('*, user:users(first_name, last_name, student_id, email)').execute()
        return result.data
    @staticmethod
    def get_new():
        result = supabase.table('feedback').select('*, user:users(first_name, last_name, student_id, email)').eq('status', 'new').execute()
        return result.data
    @staticmethod
    def create(data): return execute_db('feedback', data, operation='insert')
