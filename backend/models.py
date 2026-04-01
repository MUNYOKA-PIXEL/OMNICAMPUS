import hashlib
import jwt
import datetime
import json
from database import supabase, query_db, execute_db
from config import Config

# ==================== User Models ====================

class User:
    """User model for students"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create(student_id, first_name, last_name, email, phone, password):
        data = {
            'student_id': student_id,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'password_hash': User.hash_password(password)
        }
        return execute_db('users', data, operation='insert')
    
    @staticmethod
    def find_by_email_or_id(identifier):
        # Using Supabase or_ filter for email or student_id
        result = supabase.table('users').select('*').or_(f"email.eq.{identifier},student_id.eq.{identifier}").execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(user_id):
        return query_db('users', filters={'id': user_id}, one=True)
    
    @staticmethod
    def get_all():
        result = supabase.table('users').select('*').eq('is_active', True).order('registration_date', descending=True).execute()
        return result.data
    
    @staticmethod
    def authenticate(identifier, password):
        user = User.find_by_email_or_id(identifier)
        if user and user['password_hash'] == User.hash_password(password):
            return user
        return None
    
    @staticmethod
    def generate_token(user_id):
        payload = {
            'user_id': user_id,
            'role': 'student',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def update(user_id, **kwargs):
        if 'password' in kwargs:
            kwargs['password_hash'] = User.hash_password(kwargs.pop('password'))
        return execute_db('users', kwargs, operation='update', filters={'id': user_id})
    
    @staticmethod
    def delete(user_id):
        return execute_db('users', {'is_active': False}, operation='update', filters={'id': user_id})

# ==================== Admin Models ====================

class Admin:
    """Super admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        result = supabase.table('admins').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").eq('is_active', True).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(admin_id):
        return query_db('admins', filters={'id': admin_id}, one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = Admin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == Admin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'user_id': admin_id,  # Consistently use 'user_id' for auth.py
            'role': 'super_admin',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

class LibraryAdmin:
    """Library admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        result = supabase.table('library_admins').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").eq('is_active', True).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(admin_id):
        return query_db('library_admins', filters={'id': admin_id}, one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = LibraryAdmin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == LibraryAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'user_id': admin_id,
            'role': 'library_admin',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def get_all():
        result = supabase.table('library_admins').select('*').eq('is_active', True).execute()
        return result.data

class LostFoundAdmin:
    """Lost & Found admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        result = supabase.table('lost_found_admins').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").eq('is_active', True).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(admin_id):
        return query_db('lost_found_admins', filters={'id': admin_id}, one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = LostFoundAdmin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == LostFoundAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'user_id': admin_id,
            'role': 'lost_found_admin',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

class ClubsAdmin:
    """Clubs admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        result = supabase.table('clubs_admins').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").eq('is_active', True).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(admin_id):
        return query_db('clubs_admins', filters={'id': admin_id}, one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = ClubsAdmin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == ClubsAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'user_id': admin_id,
            'role': 'clubs_admin',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

class MedicalAdmin:
    """Medical admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        result = supabase.table('medical_admins').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").eq('is_active', True).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(admin_id):
        return query_db('medical_admins', filters={'id': admin_id}, one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = MedicalAdmin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == MedicalAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'user_id': admin_id,
            'role': 'medical_admin',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

class UserAdmin:
    """User admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        result = supabase.table('user_admins').select('*').or_(f"username.eq.{identifier},email.eq.{identifier}").eq('is_active', True).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def find_by_id(admin_id):
        return query_db('user_admins', filters={'id': admin_id}, one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = UserAdmin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == UserAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'user_id': admin_id,
            'role': 'user_admin',
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# ==================== Library Models ====================

class LibraryBook:
    """Library book model"""
    
    @staticmethod
    def get_all():
        result = supabase.table('library_books').select('*').order('title').execute()
        return result.data
    
    @staticmethod
    def get_by_id(book_id):
        return query_db('library_books', filters={'id': book_id}, one=True)
    
    @staticmethod
    def search(query):
        result = supabase.table('library_books').select('*').or_(f"title.ilike.%{query}%,author.ilike.%{query}%,isbn.ilike.%{query}%").execute()
        return result.data
    
    @staticmethod
    def create(title, author, isbn, category, total_copies, added_by=None):
        data = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'category': category,
            'total_copies': total_copies,
            'available_copies': total_copies,
            'added_by': added_by
        }
        return execute_db('library_books', data, operation='insert')
    
    @staticmethod
    def update(book_id, **kwargs):
        return execute_db('library_books', kwargs, operation='update', filters={'id': book_id})
    
    @staticmethod
    def delete(book_id):
        return execute_db('library_books', None, operation='delete', filters={'id': book_id})

class BookLoan:
    """Book loan model"""
    
    @staticmethod
    def get_current_loans():
        result = supabase.table('book_loans').select(
            '*, user:users(first_name, last_name, student_id), book:library_books(title, author)'
        ).in_('status', ['issued', 'overdue']).order('due_date').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            book = rec.pop('book')
            if book:
                rec['book_title'] = book['title']
                rec['author'] = book['author']
            data.append(rec)
        return data
    
    @staticmethod
    def get_user_loans(user_id):
        result = supabase.table('book_loans').select(
            '*, book:library_books(title, author)'
        ).eq('user_id', user_id).neq('status', 'returned').order('due_date').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            book = rec.pop('book')
            if book:
                rec['book_title'] = book['title']
                rec['author'] = book['author']
            data.append(rec)
        return data
    
    @staticmethod
    def get_user_history(user_id):
        result = supabase.table('book_loans').select(
            '*, book:library_books(title, author)'
        ).eq('user_id', user_id).order('issue_date', descending=True).execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            book = rec.pop('book')
            if book:
                rec['book_title'] = book['title']
                rec['author'] = book['author']
            data.append(rec)
        return data
    
    @staticmethod
    def issue_book(user_id, book_id, due_date, issued_by=None):
        book = LibraryBook.get_by_id(book_id)
        if not book or book['available_copies'] <= 0:
            return False
        
        data = {
            'user_id': user_id,
            'book_id': book_id,
            'due_date': due_date,
            'status': 'issued',
            'issued_by': issued_by
        }
        loan_id = execute_db('book_loans', data, operation='insert')
        
        if loan_id:
            LibraryBook.update(book_id, available_copies=book['available_copies'] - 1)
        
        return loan_id
    
    @staticmethod
    def return_book(loan_id, returned_by=None):
        loan = query_db('book_loans', filters={'id': loan_id}, one=True)
        if not loan or loan['status'] == 'returned':
            return False
        
        due_date = datetime.datetime.strptime(loan['due_date'].split('T')[0], '%Y-%m-%d')
        today = datetime.datetime.now()
        if due_date < today:
            days_overdue = (today - due_date).days
            fine_amount = days_overdue * 50
        else:
            fine_amount = 0
        
        data = {
            'return_date': datetime.datetime.utcnow().isoformat(),
            'status': 'returned',
            'fine_amount': fine_amount,
            'returned_to': returned_by
        }
        execute_db('book_loans', data, operation='update', filters={'id': loan_id})
        
        book = LibraryBook.get_by_id(loan['book_id'])
        if book:
            LibraryBook.update(book['id'], available_copies=book['available_copies'] + 1)
        
        return True
    
    @staticmethod
    def pay_fine(loan_id):
        return execute_db('book_loans', {'fine_paid': True}, operation='update', filters={'id': loan_id})

class BookRequest:
    """Book request model"""
    
    @staticmethod
    def create(user_id, book_title, book_author):
        data = {
            'user_id': user_id,
            'book_title': book_title,
            'book_author': book_author
        }
        return execute_db('book_requests', data, operation='insert')
    
    @staticmethod
    def get_pending():
        result = supabase.table('book_requests').select(
            '*, user:users(first_name, last_name, student_id, email)'
        ).eq('status', 'pending').order('request_date').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def get_user_requests(user_id):
        result = supabase.table('book_requests').select('*').eq('user_id', user_id).order('request_date', descending=True).execute()
        return result.data
    
    @staticmethod
    def approve(request_id, admin_id):
        data = {
            'status': 'approved',
            'processed_by': admin_id,
            'processed_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('book_requests', data, operation='update', filters={'id': request_id})
    
    @staticmethod
    def reject(request_id, admin_id, notes):
        data = {
            'status': 'rejected',
            'processed_by': admin_id,
            'processed_date': datetime.datetime.utcnow().isoformat(),
            'admin_notes': notes
        }
        return execute_db('book_requests', data, operation='update', filters={'id': request_id})

# ==================== Lost & Found Models ====================

class LostItem:
    """Lost item model"""
    
    @staticmethod
    def get_all():
        result = supabase.table('lost_items').select(
            '*, user:users(first_name, last_name, student_id)'
        ).eq('status', 'lost').order('reported_date', descending=True).execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def get_by_id(item_id):
        return query_db('lost_items', filters={'id': item_id}, one=True)
    
    @staticmethod
    def get_user_items(user_id):
        result = supabase.table('lost_items').select('*').eq('user_id', user_id).order('reported_date', descending=True).execute()
        return result.data
    
    @staticmethod
    def create(user_id, item_name, description, category, location_lost, date_lost):
        data = {
            'user_id': user_id,
            'item_name': item_name,
            'description': description,
            'category': category,
            'location_lost': location_lost,
            'date_lost': date_lost
        }
        return execute_db('lost_items', data, operation='insert')
    
    @staticmethod
    def verify(item_id, admin_id):
        data = {
            'status': 'verified',
            'verified_by': admin_id,
            'verified_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('lost_items', data, operation='update', filters={'id': item_id})
    
    @staticmethod
    def delete(item_id):
        return execute_db('lost_items', None, operation='delete', filters={'id': item_id})

class FoundItem:
    """Found item model"""
    
    @staticmethod
    def get_all():
        result = supabase.table('found_items').select(
            '*, user:users(first_name, last_name, student_id)'
        ).eq('status', 'found').order('reported_date', descending=True).execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def get_by_id(item_id):
        return query_db('found_items', filters={'id': item_id}, one=True)
    
    @staticmethod
    def get_user_items(user_id):
        result = supabase.table('found_items').select('*').eq('user_id', user_id).order('reported_date', descending=True).execute()
        return result.data
    
    @staticmethod
    def create(user_id, item_name, description, category, location_found, date_found):
        data = {
            'user_id': user_id,
            'item_name': item_name,
            'description': description,
            'category': category,
            'location_found': location_found,
            'date_found': date_found
        }
        return execute_db('found_items', data, operation='insert')
    
    @staticmethod
    def verify(item_id, admin_id):
        data = {
            'status': 'verified',
            'verified_by': admin_id,
            'verified_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('found_items', data, operation='update', filters={'id': item_id})
    
    @staticmethod
    def mark_returned(item_id, admin_id):
        data = {
            'status': 'returned',
            'verified_by': admin_id,
            'verified_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('found_items', data, operation='update', filters={'id': item_id})
    
    @staticmethod
    def delete(item_id):
        return execute_db('found_items', None, operation='delete', filters={'id': item_id})

class LostItemClaim:
    """Lost item claim model"""
    
    @staticmethod
    def create(lost_item_id, claimer_id):
        data = {
            'lost_item_id': lost_item_id,
            'claimer_id': claimer_id
        }
        return execute_db('lost_item_claims', data, operation='insert')
    
    @staticmethod
    def get_pending():
        result = supabase.table('lost_item_claims').select(
            '*, item:lost_items(item_name, description), user:users(first_name, last_name, student_id)'
        ).eq('status', 'pending').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            item = rec.pop('item')
            if item:
                rec.update(item)
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def approve(claim_id, admin_id):
        data = {
            'status': 'approved',
            'processed_by': admin_id,
            'processed_date': datetime.datetime.utcnow().isoformat()
        }
        execute_db('lost_item_claims', data, operation='update', filters={'id': claim_id})
        
        claim = query_db('lost_item_claims', filters={'id': claim_id}, one=True)
        if claim:
            execute_db('lost_items', {'status': 'claimed'}, operation='update', filters={'id': claim['lost_item_id']})
    
    @staticmethod
    def reject(claim_id, admin_id, notes):
        data = {
            'status': 'rejected',
            'processed_by': admin_id,
            'processed_date': datetime.datetime.utcnow().isoformat(),
            'admin_notes': notes
        }
        return execute_db('lost_item_claims', data, operation='update', filters={'id': claim_id})

class FoundItemClaim:
    """Found item claim model"""
    
    @staticmethod
    def create(found_item_id, claimant_id):
        data = {
            'found_item_id': found_item_id,
            'claimant_id': claimant_id
        }
        return execute_db('found_item_claims', data, operation='insert')
    
    @staticmethod
    def get_pending():
        result = supabase.table('found_item_claims').select(
            '*, item:found_items(item_name, description), user:users(first_name, last_name, student_id)'
        ).eq('status', 'pending').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            item = rec.pop('item')
            if item:
                rec.update(item)
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def approve(claim_id, admin_id):
        data = {
            'status': 'approved',
            'processed_by': admin_id,
            'processed_date': datetime.datetime.utcnow().isoformat()
        }
        execute_db('found_item_claims', data, operation='update', filters={'id': claim_id})
        
        claim = query_db('found_item_claims', filters={'id': claim_id}, one=True)
        if claim:
            execute_db('found_items', {'status': 'claimed'}, operation='update', filters={'id': claim['found_item_id']})
    
    @staticmethod
    def reject(claim_id, admin_id, notes):
        data = {
            'status': 'rejected',
            'processed_by': admin_id,
            'processed_date': datetime.datetime.utcnow().isoformat(),
            'admin_notes': notes
        }
        return execute_db('found_item_claims', data, operation='update', filters={'id': claim_id})

# ==================== Clubs Models ====================

class Club:
    """Club model"""
    
    @staticmethod
    def get_all():
        result = supabase.table('clubs').select('*').eq('status', 'active').order('name').execute()
        return result.data
    
    @staticmethod
    def get_pending():
        result = supabase.table('clubs').select('*').eq('status', 'pending').order('created_at').execute()
        return result.data
    
    @staticmethod
    def get_by_id(club_id):
        return query_db('clubs', filters={'id': club_id}, one=True)
    
    @staticmethod
    def create(name, description, category, contact_email, dues_amount=0, created_by=None):
        data = {
            'name': name,
            'description': description,
            'category': category,
            'contact_email': contact_email,
            'dues_amount': dues_amount,
            'status': 'pending',
            'created_by': created_by
        }
        return execute_db('clubs', data, operation='insert')
    
    @staticmethod
    def approve(club_id, admin_id):
        data = {
            'status': 'active',
            'approved_by': admin_id,
            'approved_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('clubs', data, operation='update', filters={'id': club_id})
    
    @staticmethod
    def update(club_id, **kwargs):
        return execute_db('clubs', kwargs, operation='update', filters={'id': club_id})
    
    @staticmethod
    def delete(club_id):
        return execute_db('clubs', None, operation='delete', filters={'id': club_id})
    
    @staticmethod
    def get_members(club_id):
        result = supabase.table('club_memberships').select(
            '*, user:users(first_name, last_name, email, student_id)'
        ).eq('club_id', club_id).eq('status', 'active').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data
    
    @staticmethod
    def add_member(club_id, user_id, role='member'):
        existing = supabase.table('club_memberships').select('*').eq('club_id', club_id).eq('user_id', user_id).execute()
        
        if existing.data:
            membership = existing.data[0]
            if membership['status'] == 'inactive':
                execute_db('club_memberships', {'status': 'active'}, operation='update', filters={'id': membership['id']})
                return membership['id']
            else:
                return membership['id']
        
        data = {
            'club_id': club_id,
            'user_id': user_id,
            'role': role,
            'status': 'pending'
        }
        return execute_db('club_memberships', data, operation='insert')
    
    @staticmethod
    def approve_member(membership_id, admin_id):
        data = {
            'status': 'active',
            'approved_by': admin_id,
            'approved_date': datetime.datetime.utcnow().isoformat()
        }
        execute_db('club_memberships', data, operation='update', filters={'id': membership_id})
        
        membership = query_db('club_memberships', filters={'id': membership_id}, one=True)
        if membership:
            club = Club.get_by_id(membership['club_id'])
            if club:
                Club.update(club['id'], members=club['members'] + 1)
    
    @staticmethod
    def remove_member(club_id, user_id):
        execute_db('club_memberships', {'status': 'inactive'}, operation='update', filters={'club_id': club_id, 'user_id': user_id})
        club = Club.get_by_id(club_id)
        if club:
            Club.update(club_id, members=max(0, club['members'] - 1))
    
    @staticmethod
    def pay_dues(club_id, user_id, amount):
        data = {
            'dues_paid': True,
            'dues_amount': amount,
            'dues_paid_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('club_memberships', data, operation='update', filters={'club_id': club_id, 'user_id': user_id})

class ClubMembership:
    """Club membership model"""
    
    @staticmethod
    def get_user_memberships(user_id):
        result = supabase.table('club_memberships').select(
            '*, club:clubs(name, category)'
        ).eq('user_id', user_id).eq('status', 'active').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            club = rec.pop('club')
            if club:
                rec['club_name'] = club['name']
                rec['category'] = club['category']
            data.append(rec)
        return data
    
    @staticmethod
    def get_pending_requests():
        result = supabase.table('club_memberships').select(
            '*, club:clubs(name), user:users(first_name, last_name, student_id)'
        ).eq('status', 'pending').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            club = rec.pop('club')
            if club:
                rec['club_name'] = club['name']
            user = rec.pop('user')
            if user:
                rec.update(user)
            data.append(rec)
        return data

class ClubEvent:
    """Club event model"""
    
    @staticmethod
    def get_upcoming():
        result = supabase.table('club_events').select(
            '*, club:clubs(name)'
        ).gt('event_date', datetime.datetime.utcnow().isoformat()).eq('status', 'upcoming').order('event_date').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            club = rec.pop('club')
            if club:
                rec['club_name'] = club['name']
            data.append(rec)
        return data
    
    @staticmethod
    def get_by_club(club_id):
        result = supabase.table('club_events').select('*').eq('club_id', club_id).order('event_date').execute()
        return result.data
    
    @staticmethod
    def create(club_id, title, description, event_date, location, max_participants, created_by):
        data = {
            'club_id': club_id,
            'title': title,
            'description': description,
            'event_date': event_date,
            'location': location,
            'max_participants': max_participants,
            'created_by': created_by
        }
        return execute_db('club_events', data, operation='insert')
    
    @staticmethod
    def approve(event_id, admin_id):
        data = {
            'status': 'upcoming',
            'approved_by': admin_id,
            'approved_date': datetime.datetime.utcnow().isoformat()
        }
        return execute_db('club_events', data, operation='update', filters={'id': event_id})
    
    @staticmethod
    def rsvp(event_id, user_id):
        existing = supabase.table('event_rsvps').select('*').eq('event_id', event_id).eq('user_id', user_id).execute()
        if existing.data:
            return existing.data[0]['id']
        
        event = query_db('club_events', filters={'id': event_id}, one=True)
        if event and event['max_participants'] and event['current_participants'] >= event['max_participants']:
            return False
        
        data = {'event_id': event_id, 'user_id': user_id}
        rsvp_id = execute_db('event_rsvps', data, operation='insert')
        
        if rsvp_id:
            execute_db('club_events', {'current_participants': event['current_participants'] + 1}, operation='update', filters={'id': event_id})
        
        return rsvp_id
    
    @staticmethod
    def cancel_rsvp(event_id, user_id):
        execute_db('event_rsvps', None, operation='delete', filters={'event_id': event_id, 'user_id': user_id})
        event = query_db('club_events', filters={'id': event_id}, one=True)
        if event:
            execute_db('club_events', {'current_participants': max(0, event['current_participants'] - 1)}, operation='update', filters={'id': event_id})

# ==================== Medical Models ====================

class Doctor:
    """Doctor model"""
    
    @staticmethod
    def get_all():
        result = supabase.table('doctors').select('*').order('name').execute()
        return result.data
    
    @staticmethod
    def get_available():
        result = supabase.table('doctors').select('*').eq('available', True).order('name').execute()
        return result.data
    
    @staticmethod
    def get_by_id(doctor_id):
        return query_db('doctors', filters={'id': doctor_id}, one=True)
    
    @staticmethod
    def create(name, specialty, email, phone, education, experience, languages, created_by=None):
        data = {
            'name': name,
            'specialty': specialty,
            'email': email,
            'phone': phone,
            'education': education,
            'experience': experience,
            'languages': json.dumps(languages) if languages else None,
            'created_by': created_by
        }
        return execute_db('doctors', data, operation='insert')
    
    @staticmethod
    def update(doctor_id, **kwargs):
        if 'languages' in kwargs and isinstance(kwargs['languages'], list):
            kwargs['languages'] = json.dumps(kwargs['languages'])
        kwargs['updated_at'] = datetime.datetime.utcnow().isoformat()
        return execute_db('doctors', kwargs, operation='update', filters={'id': doctor_id})
    
    @staticmethod
    def toggle_availability(doctor_id):
        doctor = Doctor.get_by_id(doctor_id)
        if doctor:
            new_status = not doctor['available']
            execute_db('doctors', {'available': new_status}, operation='update', filters={'id': doctor_id})
            return new_status
        return None

class Appointment:
    """Appointment model"""
    
    @staticmethod
    def get_upcoming():
        result = supabase.table('appointments').select(
            '*, user:users(first_name, last_name, student_id), doctor:doctors(name, specialty)'
        ).eq('status', 'upcoming').gte('appointment_date', datetime.datetime.utcnow().date().isoformat()).order('appointment_date').order('appointment_time').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            user = rec.pop('user')
            if user:
                rec.update(user)
            doctor = rec.pop('doctor')
            if doctor:
                rec['doctor_name'] = doctor['name']
                rec['specialty'] = doctor['specialty']
            data.append(rec)
        return data
    
    @staticmethod
    def get_user_appointments(user_id):
        result = supabase.table('appointments').select(
            '*, doctor:doctors(name, specialty)'
        ).eq('user_id', user_id).order('appointment_date', descending=True).execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            doctor = rec.pop('doctor')
            if doctor:
                rec['doctor_name'] = doctor['name']
                rec['specialty'] = doctor['specialty']
            data.append(rec)
        return data
    
    @staticmethod
    def create(user_id, doctor_id, service_type, appointment_date, appointment_time, reason, created_by=None):
        data = {
            'user_id': user_id,
            'doctor_id': doctor_id,
            'service_type': service_type,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'reason': reason,
            'created_by': created_by
        }
        return execute_db('appointments', data, operation='insert')
    
    @staticmethod
    def confirm(appointment_id, admin_id):
        return execute_db('appointments', {'status': 'confirmed'}, operation='update', filters={'id': appointment_id})
    
    @staticmethod
    def cancel(appointment_id, admin_id, reason):
        data = {
            'status': 'cancelled',
            'cancelled_by': admin_id,
            'cancelled_date': datetime.datetime.utcnow().isoformat(),
            'cancellation_reason': reason
        }
        return execute_db('appointments', data, operation='update', filters={'id': appointment_id})
    
    @staticmethod
    def complete(appointment_id):
        return execute_db('appointments', {'status': 'completed'}, operation='update', filters={'id': appointment_id})

class Medication:
    """Medication model"""
    
    @staticmethod
    def get_all():
        result = supabase.table('medications').select('*').order('name').execute()
        return result.data
    
    @staticmethod
    def get_available():
        result = supabase.table('medications').select('*').gt('stock', 0).order('name').execute()
        return result.data
    
    @staticmethod
    def get_by_id(medication_id):
        return query_db('medications', filters={'id': medication_id}, one=True)
    
    @staticmethod
    def create(name, description, category, price, stock, requires_prescription, created_by=None):
        data = {
            'name': name,
            'description': description,
            'category': category,
            'price': price,
            'stock': stock,
            'requires_prescription': requires_prescription,
            'created_by': created_by
        }
        return execute_db('medications', data, operation='insert')
    
    @staticmethod
    def update(medication_id, **kwargs):
        kwargs['updated_at'] = datetime.datetime.utcnow().isoformat()
        return execute_db('medications', kwargs, operation='update', filters={'id': medication_id})
    
    @staticmethod
    def update_stock(medication_id, quantity):
        med = Medication.get_by_id(medication_id)
        if med:
            return Medication.update(medication_id, stock=med['stock'] + quantity)
        return None

class Prescription:
    """Prescription model"""
    
    @staticmethod
    def get_user_prescriptions(user_id):
        result = supabase.table('prescriptions').select(
            '*, doctor:doctors(name), medication:medications(name, description)'
        ).eq('user_id', user_id).eq('status', 'active').order('expiry_date').execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            doctor = rec.pop('doctor')
            if doctor:
                rec['doctor_name'] = doctor['name']
            medication = rec.pop('medication')
            if medication:
                rec['medication_name'] = medication['name']
                rec['medication_description'] = medication['description']
            data.append(rec)
        return data
    
    @staticmethod
    def create(user_id, doctor_id, medication_id, dosage, instructions, prescribed_date, expiry_date, refills, created_by=None):
        data = {
            'user_id': user_id,
            'doctor_id': doctor_id,
            'medication_id': medication_id,
            'dosage': dosage,
            'instructions': instructions,
            'prescribed_date': prescribed_date,
            'expiry_date': expiry_date,
            'refills': refills,
            'created_by': created_by
        }
        return execute_db('prescriptions', data, operation='insert')
    
    @staticmethod
    def request_refill(prescription_id):
        data = {'prescription_id': prescription_id}
        return execute_db('prescription_refills', data, operation='insert')
    
    @staticmethod
    def approve_refill(refill_id, admin_id):
        refill = query_db('prescription_refills', filters={'id': refill_id}, one=True)
        if not refill:
            return False
        
        prescription = query_db('prescriptions', filters={'id': refill['prescription_id']}, one=True)
        if not prescription or prescription['refills_used'] >= prescription['refills']:
            return False
        
        data = {
            'status': 'approved',
            'approved_by': admin_id,
            'approved_date': datetime.datetime.utcnow().isoformat()
        }
        execute_db('prescription_refills', data, operation='update', filters={'id': refill_id})
        
        execute_db('prescriptions', {'refills_used': prescription['refills_used'] + 1}, operation='update', filters={'id': prescription['id']})
        
        return True

class MedicalRecord:
    """Medical record model"""
    
    @staticmethod
    def get_user_records(user_id):
        result = supabase.table('medical_records').select(
            '*, doctor:doctors(name)'
        ).eq('user_id', user_id).order('record_date', descending=True).execute()
        
        data = []
        for row in result.data:
            rec = row.copy()
            doctor = rec.pop('doctor')
            if doctor:
                rec['doctor_name'] = doctor['name']
            data.append(rec)
        return data
    
    @staticmethod
    def create(user_id, record_type, record_date, doctor_id, diagnosis, notes, created_by=None):
        data = {
            'user_id': user_id,
            'record_type': record_type,
            'record_date': record_date,
            'doctor_id': doctor_id,
            'diagnosis': diagnosis,
            'notes': notes,
            'created_by': created_by
        }
        return execute_db('medical_records', data, operation='insert')

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
