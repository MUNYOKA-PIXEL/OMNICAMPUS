import datetime
from .database import get_db, execute_db, query_db

# Initialize the Supabase client
supabase = get_db()

# ==================== User Models ====================

class User:
    """User/Student model"""
    
    @staticmethod
    def create(data):
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
    def get_all():
        return query_db('users')

class Admin:
    """Admin model"""
    
    @staticmethod
    def find_by_username(username):
        return query_db('admins', filters={'username': username}, one=True)
    
    @staticmethod
    def find_by_email(email):
        return query_db('admins', filters={'email': email}, one=True)
    
    @staticmethod
    def find_by_username_or_email(value):
        # Querying by username or email
        admin = query_db('admins', filters={'username': value}, one=True)
        if not admin:
            admin = query_db('admins', filters={'email': value}, one=True)
        return admin
    
    @staticmethod
    def get_all():
        return query_db('admins')

# ==================== Library Models ====================

class LibraryBook:
    """Library book model"""
    
    @staticmethod
    def get_all():
        return query_db('books')
    
    @staticmethod
    def find_by_id(book_id):
        return query_db('books', filters={'id': book_id}, one=True)
    
    @staticmethod
    def search(query):
        result = supabase.table('books').select('*').ilike('title', f'%{query}%').execute()
        if not result.data:
            result = supabase.table('books').select('*').ilike('author', f'%{query}%').execute()
        return result.data
    
    @staticmethod
    def create(data):
        return execute_db('books', data, operation='insert')

class BookLoan:
    """Library book loan model"""
    
    @staticmethod
    def get_by_user(user_id):
        return query_db('loans', filters={'user_id': user_id})
    
    @staticmethod
    def create(data):
        return execute_db('loans', data, operation='insert')

# ==================== Lost & Found Models ====================

class LostItem:
    """Lost item model"""
    
    @staticmethod
    def get_all():
        return query_db('lost_items')
    
    @staticmethod
    def create(data):
        return execute_db('lost_items', data, operation='insert')

class FoundItem:
    """Found item model"""
    
    @staticmethod
    def get_all():
        return query_db('found_items')
    
    @staticmethod
    def create(data):
        return execute_db('found_items', data, operation='insert')

# ==================== Club Models ====================

class Club:
    """Student club model"""
    
    @staticmethod
    def get_all():
        return query_db('clubs')
    
    @staticmethod
    def find_by_id(club_id):
        return query_db('clubs', filters={'id': club_id}, one=True)

class ClubMembership:
    """Club membership model"""
    
    @staticmethod
    def get_by_user(user_id):
        return query_db('club_memberships', filters={'user_id': user_id})
    
    @staticmethod
    def create(data):
        return execute_db('club_memberships', data, operation='insert')

# ==================== Feedback Model ====================

class Feedback:
    """Feedback model"""
    
    @staticmethod
    def create(user_id, category, message):
        data = {
            'user_id': user_id,
            'category': category,
            'message': message
        }
        return execute_db('feedback', data, operation='insert')
    
    @staticmethod
    def get_all():
        result = supabase.table('feedback').select(
            '*, user:users(first_name, last_name, student_id, email)'
        ).order('submitted_date', descending=True).execute()
        
        data = []
        if result.data:
            for row in result.data:
                rec = row.copy()
                user = rec.pop('user')
                if user:
                    rec.update(user)
                data.append(rec)
        return data
    
    @staticmethod
    def get_new():
        result = supabase.table('feedback').select(
            '*, user:users(first_name, last_name, student_id, email)'
        ).eq('status', 'new').order('submitted_date').execute()
        
        data = []
        if result.data:
            for row in result.data:
                rec = row.copy()
                user = rec.pop('user')
                if user:
                    rec.update(user)
                data.append(rec)
        return data
    
    @staticmethod
    def respond(feedback_id, admin_id, response):
        data = {
            'status': 'replied',
            'admin_response': response,
            'responded_by': admin_id,
            'responded_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('feedback', data, operation='update', filters={'id': feedback_id})
