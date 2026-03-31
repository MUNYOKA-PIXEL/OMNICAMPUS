import datetime
import jwt
import bcrypt
from .database import get_db, execute_db, query_db

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
    def get_user_loans(user_id): return query_db('loans', filters={'user_id': user_id, 'status': 'issued'})
    @staticmethod
    def get_user_history(user_id): return query_db('loans', filters={'user_id': user_id})
    @staticmethod
    def issue_book(user_id, book_id, due_date, issued_by=None):
        # Check book availability
        book = LibraryBook.find_by_id(book_id)
        if not book or book['available_copies'] <= 0:
            return None
        
        # Create loan record
        data = {
            'user_id': user_id,
            'book_id': book_id,
            'issue_date': datetime.datetime.utcnow().isoformat(),
            'due_date': due_date,
            'status': 'issued',
            'issued_by': issued_by
        }
        loan_id = execute_db('loans', data, operation='insert')
        
        # Decrement available copies
        supabase.table('books').update({'available_copies': book['available_copies'] - 1}).eq('id', book_id).execute()
        
        return loan_id

    @staticmethod
    def return_book(loan_id, returned_by=None):
        loan = query_db('loans', filters={'id': loan_id}, one=True)
        if not loan or loan['status'] == 'returned':
            return False
        
        # Update loan status and return date
        execute_db('loans', {'status': 'returned', 'return_date': datetime.datetime.utcnow().isoformat(), 'returned_by': returned_by}, operation='update', filters={'id': loan_id})
        
        # Increment available copies
        book = LibraryBook.find_by_id(loan['book_id'])
        if book:
            supabase.table('books').update({'available_copies': book['available_copies'] + 1}).eq('id', loan['book_id']).execute()
        
        return True

class BookRequest:
    @staticmethod
    def get_all(): return query_db('book_requests')
    @staticmethod
    def get_pending(): return query_db('book_requests', filters={'status': 'pending'})
    @staticmethod
    def get_user_requests(user_id): return query_db('book_requests', filters={'user_id': user_id})
    @staticmethod
    def create(data): return execute_db('book_requests', data, operation='insert')
    @staticmethod
    def approve(request_id, approved_by=None):
        return execute_db('book_requests', {'status': 'approved', 'approved_by': approved_by, 'approval_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': request_id})
    @staticmethod
    def reject(request_id, rejected_by=None, notes=''):
        return execute_db('book_requests', {'status': 'rejected', 'rejected_by': rejected_by, 'rejection_notes': notes, 'rejection_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': request_id})

# ==================== Lost & Found Models ====================

class LostItem:
    @staticmethod
    def get_all(): return query_db('lost_items')
    @staticmethod
    def get_user_items(user_id): return query_db('lost_items', filters={'user_id': user_id})
    @staticmethod
    def create(data): return execute_db('lost_items', data, operation='insert')
    @staticmethod
    def update_status(item_id, status): return execute_db('lost_items', {'status': status}, operation='update', filters={'id': item_id})
    @staticmethod
    def delete(item_id): return execute_db('lost_items', {}, operation='delete', filters={'id': item_id})

class FoundItem:
    @staticmethod
    def get_all(): return query_db('found_items')
    @staticmethod
    def get_user_items(user_id): return query_db('found_items', filters={'user_id': user_id})
    @staticmethod
    def create(data): return execute_db('found_items', data, operation='insert')
    @staticmethod
    def update_status(item_id, status): return execute_db('found_items', {'status': status}, operation='update', filters={'id': item_id})
    @staticmethod
    def mark_returned(item_id, returned_by=None): return execute_db('found_items', {'status': 'returned', 'returned_by': returned_by, 'return_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': item_id})
    @staticmethod
    def delete(item_id): return execute_db('found_items', {}, operation='delete', filters={'id': item_id})


class LostItemClaim:
    @staticmethod
    def get_pending(): return query_db('lost_item_claims', filters={'status': 'pending'})
    @staticmethod
    def create(item_id, user_id):
        data = {'lost_item_id': item_id, 'user_id': user_id, 'claim_date': datetime.datetime.utcnow().isoformat(), 'status': 'pending'}
        return execute_db('lost_item_claims', data, operation='insert')
    @staticmethod
    def approve(claim_id, approved_by=None): return execute_db('lost_item_claims', {'status': 'approved', 'approved_by': approved_by, 'approval_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': claim_id})
    @staticmethod
    def reject(claim_id, rejected_by=None, notes=''): return execute_db('lost_item_claims', {'status': 'rejected', 'rejected_by': rejected_by, 'rejection_notes': notes, 'rejection_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': claim_id})

class FoundItemClaim:
    @staticmethod
    def get_pending(): return query_db('found_item_claims', filters={'status': 'pending'})
    @staticmethod
    def create(item_id, user_id):
        data = {'found_item_id': item_id, 'user_id': user_id, 'claim_date': datetime.datetime.utcnow().isoformat(), 'status': 'pending'}
        return execute_db('found_item_claims', data, operation='insert')
    @staticmethod
    def approve(claim_id, approved_by=None): return execute_db('found_item_claims', {'status': 'approved', 'approved_by': approved_by, 'approval_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': claim_id})
    @staticmethod
    def reject(claim_id, rejected_by=None, notes=''): return execute_db('found_item_claims', {'status': 'rejected', 'rejected_by': rejected_by, 'rejection_notes': notes, 'rejection_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': claim_id})

# ==================== Club Models ====================

class Club:
    @staticmethod
    def get_all(): return query_db('clubs')
    @staticmethod
    def get_pending(): return query_db('clubs', filters={'status': 'pending'})
    @staticmethod
    def get_by_id(club_id): return query_db('clubs', filters={'id': club_id}, one=True)
    @staticmethod
    def create(data): return execute_db('clubs', data, operation='insert')
    @staticmethod
    def update(club_id, **kwargs): return execute_db('clubs', kwargs, operation='update', filters={'id': club_id})
    @staticmethod
    def delete(club_id): return execute_db('clubs', {}, operation='delete', filters={'id': club_id})
    @staticmethod
    def approve(club_id, approved_by=None): return execute_db('clubs', {'status': 'approved', 'approved_by': approved_by, 'approval_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': club_id})
    @staticmethod
    def add_member(club_id, user_id):
        data = {'club_id': club_id, 'user_id': user_id, 'join_date': datetime.datetime.utcnow().isoformat(), 'status': 'pending'}
        return execute_db('club_memberships', data, operation='insert')
    @staticmethod
    def remove_member(club_id, user_id): return execute_db('club_memberships', {}, operation='delete', filters={'club_id': club_id, 'user_id': user_id})
    @staticmethod
    def pay_dues(club_id, user_id, amount):
        data = {'club_id': club_id, 'user_id': user_id, 'payment_date': datetime.datetime.utcnow().isoformat(), 'amount': amount}
        return execute_db('club_dues', data, operation='insert')

class ClubEvent:
    @staticmethod
    def get_all(): return query_db('club_events')
    @staticmethod
    def get_upcoming():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return supabase.table('club_events').select('*').gte('event_date', today).execute().data
    @staticmethod
    def get_by_club(club_id): return query_db('club_events', filters={'club_id': club_id})
    @staticmethod
    def rsvp(event_id, user_id):
        # Check if event is full
        event = supabase.table('club_events').select('*').eq('id', event_id).single().execute().data
        if not event or event['current_attendees'] >= event['max_attendees']:
            return None
        
        # Create RSVP record
        data = {'event_id': event_id, 'user_id': user_id, 'rsvp_date': datetime.datetime.utcnow().isoformat()}
        rsvp_id = execute_db('event_rsvps', data, operation='insert')
        
        # Increment current attendees
        supabase.table('club_events').update({'current_attendees': event['current_attendees'] + 1}).eq('id', event_id).execute()
        
        return rsvp_id
    @staticmethod
    def cancel_rsvp(event_id, user_id):
        # Decrement current attendees
        event = supabase.table('club_events').select('current_attendees', 'id').eq('id', event_id).single().execute().data
        if event and event.data and event.data['current_attendees'] > 0:
            supabase.table('club_events').update({'current_attendees': event.data['current_attendees'] - 1}).eq('id', event_id).execute()
        
        # Delete RSVP record
        return execute_db('event_rsvps', {}, operation='delete', filters={'event_id': event_id, 'user_id': user_id})

class ClubMembership:
    @staticmethod
    def get_by_user(user_id): return query_db('club_memberships', filters={'user_id': user_id})
    @staticmethod
    def get_pending_requests(): return query_db('club_memberships', filters={'status': 'pending'})

# ==================== Medical Models ====================

class Doctor:
    @staticmethod
    def get_all(): return query_db('doctors')
    @staticmethod
    def get_available(): return query_db('doctors', filters={'is_available': True})
    @staticmethod
    def get_by_id(doctor_id): return query_db('doctors', filters={'id': doctor_id}, one=True)

class Appointment:
    @staticmethod
    def get_all(): return query_db('appointments')
    @staticmethod
    def get_upcoming():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return supabase.table('appointments').select('*').gte('appointment_date', today).execute().data
    @staticmethod
    def get_user_appointments(user_id): return query_db('appointments', filters={'user_id': user_id})
    @staticmethod
    def create(data): return execute_db('appointments', data, operation='insert')
    @staticmethod
    def confirm(appointment_id, confirmed_by=None): return execute_db('appointments', {'status': 'confirmed', 'confirmed_by': confirmed_by, 'confirmation_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': appointment_id})
    @staticmethod
    def cancel(appointment_id, cancelled_by=None, reason=''): return execute_db('appointments', {'status': 'cancelled', 'cancelled_by': cancelled_by, 'cancellation_reason': reason, 'cancellation_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': appointment_id})
    @staticmethod
    def complete(appointment_id): return execute_db('appointments', {'status': 'completed'}, operation='update', filters={'id': appointment_id})

class Medication:
    @staticmethod
    def get_all(): return query_db('medications')
    @staticmethod
    def get_available(): return query_db('medications', filters={'is_available': True})
    @staticmethod
    def get_by_id(medication_id): return query_db('medications', filters={'id': medication_id}, one=True)
    @staticmethod
    def create(data): return execute_db('medications', data, operation='insert')
    @staticmethod
    def update(medication_id, **kwargs): return execute_db('medications', kwargs, operation='update', filters={'id': medication_id})
    @staticmethod
    def update_stock(medication_id, quantity): return execute_db('medications', {'stock': quantity}, operation='update', filters={'id': medication_id})

class Prescription:
    @staticmethod
    def get_all(): return query_db('prescriptions')
    @staticmethod
    def get_user_prescriptions(user_id): return query_db('prescriptions', filters={'user_id': user_id})
    @staticmethod
    def create(data): return execute_db('prescriptions', data, operation='insert')
    @staticmethod
    def request_refill(prescription_id):
        # For now, just mark as pending refill
        return execute_db('prescriptions', {'refill_requested': True, 'refill_requested_date': datetime.datetime.utcnow().isoformat()}, operation='update', filters={'id': prescription_id})

class MedicalRecord:
    @staticmethod
    def get_all(): return query_db('medical_records')
    @staticmethod
    def get_user_records(user_id): return query_db('medical_records', filters={'user_id': user_id})
    @staticmethod
    def create(data): return execute_db('medical_records', data, operation='insert')

# ==================== Feedback Model ====================

class Feedback:
    @staticmethod
    def get_all():
        result = supabase.table('feedback').select('*, user:users(first_name, last_name, student_id, email)').execute()
        if result.data:
            data = []
            for row in result.data:
                rec = row.copy()
                user = rec.pop('user')
                if user:
                    rec.update(user)
                data.append(rec)
            return data
        return []
    
    @staticmethod
    def get_new():
        result = supabase.table('feedback').select('*, user:users(first_name, last_name, student_id, email)').eq('status', 'new').order('submitted_date').execute()
        if result.data:
            data = []
            for row in result.data:
                rec = row.copy()
                user = rec.pop('user')
                if user:
                    rec.update(user)
                data.append(rec)
            return data
        return []

    @staticmethod
    def create(data):
        data['submitted_date'] = datetime.datetime.utcnow().isoformat()
        data['status'] = 'new'
        return execute_db('feedback', data, operation='insert')
    
    @staticmethod
    def respond(feedback_id, admin_id, response):
        data = {
            'status': 'replied',
            'admin_response': response,
            'responded_by': admin_id,
            'responded_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('feedback', data, operation='update', filters={'id': feedback_id})
