import hashlib
import jwt
import datetime
import json
from database import query_db, execute_db
from config import Config

# ==================== User Models ====================

class User:
    """User model for students"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create(student_id, first_name, last_name, email, phone, password):
        password_hash = User.hash_password(password)
        query = """
            INSERT INTO users (student_id, first_name, last_name, email, phone, password_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        user_id = execute_db(query, (student_id, first_name, last_name, email, phone, password_hash))
        return user_id
    
    @staticmethod
    def find_by_email_or_id(identifier):
        query = "SELECT * FROM users WHERE email = ? OR student_id = ?"
        return query_db(query, (identifier, identifier), one=True)
    
    @staticmethod
    def find_by_id(user_id):
        query = "SELECT * FROM users WHERE id = ?"
        return query_db(query, (user_id,), one=True)
    
    @staticmethod
    def get_all():
        return query_db("SELECT * FROM users WHERE is_active = 1 ORDER BY registration_date DESC")
    
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            return payload['user_id'], payload['role']
        except:
            return None, None
    
    @staticmethod
    def update(user_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
        execute_db(query, tuple(values))
    
    @staticmethod
    def delete(user_id):
        execute_db("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))

# ==================== Super Admin Model ====================

class Admin:
    """Super admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username_or_email(identifier):
        query = "SELECT * FROM admins WHERE (username = ? OR email = ?) AND is_active = 1"
        return query_db(query, (identifier, identifier), one=True)
    
    @staticmethod
    def find_by_id(admin_id):
        query = "SELECT * FROM admins WHERE id = ?"
        return query_db(query, (admin_id,), one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = Admin.find_by_username_or_email(username)
        if admin and admin['password_hash'] == Admin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'admin_id': admin_id,
            'role': 'super_admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# ==================== Library Admin Model ====================

class LibraryAdmin:
    """Library admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM library_admins WHERE username = ? AND is_active = 1"
        return query_db(query, (username,), one=True)
    
    @staticmethod
    def find_by_email(email):
        query = "SELECT * FROM library_admins WHERE email = ? AND is_active = 1"
        return query_db(query, (email,), one=True)
    
    @staticmethod
    def find_by_id(admin_id):
        query = "SELECT * FROM library_admins WHERE id = ?"
        return query_db(query, (admin_id,), one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = LibraryAdmin.find_by_username(username)
        if not admin:
            admin = LibraryAdmin.find_by_email(username)
        if admin and admin['password_hash'] == LibraryAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'admin_id': admin_id,
            'role': 'library_admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    
    @staticmethod
    def get_all():
        return query_db("SELECT * FROM library_admins WHERE is_active = 1")

# ==================== Lost & Found Admin Model ====================

class LostFoundAdmin:
    """Lost & Found admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM lost_found_admins WHERE username = ? AND is_active = 1"
        return query_db(query, (username,), one=True)
    
    @staticmethod
    def find_by_email(email):
        query = "SELECT * FROM lost_found_admins WHERE email = ? AND is_active = 1"
        return query_db(query, (email,), one=True)
    
    @staticmethod
    def find_by_id(admin_id):
        query = "SELECT * FROM lost_found_admins WHERE id = ?"
        return query_db(query, (admin_id,), one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = LostFoundAdmin.find_by_username(username)
        if not admin:
            admin = LostFoundAdmin.find_by_email(username)
        if admin and admin['password_hash'] == LostFoundAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'admin_id': admin_id,
            'role': 'lost_found_admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# ==================== Clubs Admin Model ====================

class ClubsAdmin:
    """Clubs admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM clubs_admins WHERE username = ? AND is_active = 1"
        return query_db(query, (username,), one=True)
    
    @staticmethod
    def find_by_email(email):
        query = "SELECT * FROM clubs_admins WHERE email = ? AND is_active = 1"
        return query_db(query, (email,), one=True)
    
    @staticmethod
    def find_by_id(admin_id):
        query = "SELECT * FROM clubs_admins WHERE id = ?"
        return query_db(query, (admin_id,), one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = ClubsAdmin.find_by_username(username)
        if not admin:
            admin = ClubsAdmin.find_by_email(username)
        if admin and admin['password_hash'] == ClubsAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'admin_id': admin_id,
            'role': 'clubs_admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# ==================== Medical Admin Model ====================

class MedicalAdmin:
    """Medical admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM medical_admins WHERE username = ? AND is_active = 1"
        return query_db(query, (username,), one=True)
    
    @staticmethod
    def find_by_email(email):
        query = "SELECT * FROM medical_admins WHERE email = ? AND is_active = 1"
        return query_db(query, (email,), one=True)
    
    @staticmethod
    def find_by_id(admin_id):
        query = "SELECT * FROM medical_admins WHERE id = ?"
        return query_db(query, (admin_id,), one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = MedicalAdmin.find_by_username(username)
        if not admin:
            admin = MedicalAdmin.find_by_email(username)
        if admin and admin['password_hash'] == MedicalAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'admin_id': admin_id,
            'role': 'medical_admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# ==================== User Admin Model ====================

class UserAdmin:
    """User admin model"""
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def find_by_username(username):
        query = "SELECT * FROM user_admins WHERE username = ? AND is_active = 1"
        return query_db(query, (username,), one=True)
    
    @staticmethod
    def find_by_email(email):
        query = "SELECT * FROM user_admins WHERE email = ? AND is_active = 1"
        return query_db(query, (email,), one=True)
    
    @staticmethod
    def find_by_id(admin_id):
        query = "SELECT * FROM user_admins WHERE id = ?"
        return query_db(query, (admin_id,), one=True)
    
    @staticmethod
    def authenticate(username, password):
        admin = UserAdmin.find_by_username(username)
        if not admin:
            admin = UserAdmin.find_by_email(username)
        if admin and admin['password_hash'] == UserAdmin.hash_password(password):
            return admin
        return None
    
    @staticmethod
    def generate_token(admin_id):
        payload = {
            'admin_id': admin_id,
            'role': 'user_admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

# ==================== Library Models ====================

class LibraryBook:
    """Library book model"""
    
    @staticmethod
    def get_all():
        return query_db("SELECT * FROM library_books ORDER BY title")
    
    @staticmethod
    def get_by_id(book_id):
        return query_db("SELECT * FROM library_books WHERE id = ?", (book_id,), one=True)
    
    @staticmethod
    def search(query):
        search_term = f"%{query}%"
        return query_db(
            "SELECT * FROM library_books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
            (search_term, search_term, search_term)
        )
    
    @staticmethod
    def create(title, author, isbn, category, total_copies, added_by=None):
        query = """
            INSERT INTO library_books (title, author, isbn, category, total_copies, available_copies, added_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (title, author, isbn, category, total_copies, total_copies, added_by))
    
    @staticmethod
    def update(book_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        values.append(book_id)
        query = f"UPDATE library_books SET {', '.join(fields)} WHERE id = ?"
        execute_db(query, tuple(values))
    
    @staticmethod
    def delete(book_id):
        execute_db("DELETE FROM library_books WHERE id = ?", (book_id,))

class BookLoan:
    """Book loan model"""
    
    @staticmethod
    def get_current_loans():
        return query_db("""
            SELECT bl.*, u.first_name, u.last_name, u.student_id, lb.title as book_title, lb.author
            FROM book_loans bl
            JOIN users u ON bl.user_id = u.id
            JOIN library_books lb ON bl.book_id = lb.id
            WHERE bl.status IN ('issued', 'overdue')
            ORDER BY bl.due_date
        """)
    
    @staticmethod
    def get_user_loans(user_id):
        return query_db("""
            SELECT bl.*, lb.title as book_title, lb.author
            FROM book_loans bl
            JOIN library_books lb ON bl.book_id = lb.id
            WHERE bl.user_id = ? AND bl.status != 'returned'
            ORDER BY bl.due_date
        """, (user_id,))
    
    @staticmethod
    def get_user_history(user_id):
        return query_db("""
            SELECT bl.*, lb.title as book_title, lb.author
            FROM book_loans bl
            JOIN library_books lb ON bl.book_id = lb.id
            WHERE bl.user_id = ?
            ORDER BY bl.issue_date DESC
        """, (user_id,))
    
    @staticmethod
    def issue_book(user_id, book_id, due_date, issued_by=None):
        book = LibraryBook.get_by_id(book_id)
        if not book or book['available_copies'] <= 0:
            return False
        
        query = """
            INSERT INTO book_loans (user_id, book_id, due_date, status, issued_by)
            VALUES (?, ?, ?, 'issued', ?)
        """
        loan_id = execute_db(query, (user_id, book_id, due_date, issued_by))
        
        execute_db(
            "UPDATE library_books SET available_copies = available_copies - 1 WHERE id = ?",
            (book_id,)
        )
        
        return loan_id
    
    @staticmethod
    def return_book(loan_id, returned_by=None):
        loan = query_db("SELECT * FROM book_loans WHERE id = ?", (loan_id,), one=True)
        if not loan or loan['status'] == 'returned':
            return False
        
        due_date = datetime.datetime.strptime(loan['due_date'], '%Y-%m-%d')
        today = datetime.datetime.now()
        if due_date < today:
            days_overdue = (today - due_date).days
            fine_amount = days_overdue * 50
        else:
            fine_amount = 0
        
        execute_db("""
            UPDATE book_loans 
            SET return_date = CURRENT_TIMESTAMP, 
                status = 'returned', 
                fine_amount = ?,
                returned_to = ?
            WHERE id = ?
        """, (fine_amount, returned_by, loan_id))
        
        execute_db(
            "UPDATE library_books SET available_copies = available_copies + 1 WHERE id = ?",
            (loan['book_id'],)
        )
        
        return True
    
    @staticmethod
    def pay_fine(loan_id):
        execute_db("UPDATE book_loans SET fine_paid = 1 WHERE id = ?", (loan_id,))

class BookRequest:
    """Book request model"""
    
    @staticmethod
    def create(user_id, book_title, book_author):
        query = """
            INSERT INTO book_requests (user_id, book_title, book_author)
            VALUES (?, ?, ?)
        """
        return execute_db(query, (user_id, book_title, book_author))
    
    @staticmethod
    def get_pending():
        return query_db("""
            SELECT br.*, u.first_name, u.last_name, u.student_id, u.email
            FROM book_requests br
            JOIN users u ON br.user_id = u.id
            WHERE br.status = 'pending'
            ORDER BY br.request_date
        """)
    
    @staticmethod
    def get_user_requests(user_id):
        return query_db("""
            SELECT * FROM book_requests 
            WHERE user_id = ? 
            ORDER BY request_date DESC
        """, (user_id,))
    
    @staticmethod
    def approve(request_id, admin_id):
        execute_db("""
            UPDATE book_requests 
            SET status = 'approved', 
                processed_by = ?, 
                processed_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, request_id))
    
    @staticmethod
    def reject(request_id, admin_id, notes):
        execute_db("""
            UPDATE book_requests 
            SET status = 'rejected', 
                processed_by = ?, 
                processed_date = CURRENT_TIMESTAMP,
                admin_notes = ?
            WHERE id = ?
        """, (admin_id, notes, request_id))

# ==================== Lost & Found Models ====================

class LostItem:
    """Lost item model"""
    
    @staticmethod
    def get_all():
        return query_db("""
            SELECT li.*, u.first_name, u.last_name, u.student_id
            FROM lost_items li
            JOIN users u ON li.user_id = u.id
            WHERE li.status = 'lost'
            ORDER BY li.reported_date DESC
        """)
    
    @staticmethod
    def get_by_id(item_id):
        return query_db("SELECT * FROM lost_items WHERE id = ?", (item_id,), one=True)
    
    @staticmethod
    def get_user_items(user_id):
        return query_db("""
            SELECT * FROM lost_items 
            WHERE user_id = ? 
            ORDER BY reported_date DESC
        """, (user_id,))
    
    @staticmethod
    def create(user_id, item_name, description, category, location_lost, date_lost):
        query = """
            INSERT INTO lost_items (user_id, item_name, description, category, location_lost, date_lost)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (user_id, item_name, description, category, location_lost, date_lost))
    
    @staticmethod
    def verify(item_id, admin_id):
        execute_db("""
            UPDATE lost_items 
            SET status = 'verified', 
                verified_by = ?, 
                verified_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, item_id))
    
    @staticmethod
    def delete(item_id):
        execute_db("DELETE FROM lost_items WHERE id = ?", (item_id,))

class FoundItem:
    """Found item model"""
    
    @staticmethod
    def get_all():
        return query_db("""
            SELECT fi.*, u.first_name, u.last_name, u.student_id
            FROM found_items fi
            JOIN users u ON fi.user_id = u.id
            WHERE fi.status = 'found'
            ORDER BY fi.reported_date DESC
        """)
    
    @staticmethod
    def get_by_id(item_id):
        return query_db("SELECT * FROM found_items WHERE id = ?", (item_id,), one=True)
    
    @staticmethod
    def get_user_items(user_id):
        return query_db("""
            SELECT * FROM found_items 
            WHERE user_id = ? 
            ORDER BY reported_date DESC
        """, (user_id,))
    
    @staticmethod
    def create(user_id, item_name, description, category, location_found, date_found):
        query = """
            INSERT INTO found_items (user_id, item_name, description, category, location_found, date_found)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (user_id, item_name, description, category, location_found, date_found))
    
    @staticmethod
    def verify(item_id, admin_id):
        execute_db("""
            UPDATE found_items 
            SET status = 'verified', 
                verified_by = ?, 
                verified_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, item_id))
    
    @staticmethod
    def mark_returned(item_id, admin_id):
        execute_db("""
            UPDATE found_items 
            SET status = 'returned', 
                verified_by = ?, 
                verified_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, item_id))
    
    @staticmethod
    def delete(item_id):
        execute_db("DELETE FROM found_items WHERE id = ?", (item_id,))

class LostItemClaim:
    """Lost item claim model"""
    
    @staticmethod
    def create(lost_item_id, claimer_id):
        query = """
            INSERT INTO lost_item_claims (lost_item_id, claimer_id)
            VALUES (?, ?)
        """
        return execute_db(query, (lost_item_id, claimer_id))
    
    @staticmethod
    def get_pending():
        return query_db("""
            SELECT lic.*, li.item_name, li.description, u.first_name, u.last_name, u.student_id
            FROM lost_item_claims lic
            JOIN lost_items li ON lic.lost_item_id = li.id
            JOIN users u ON lic.claimer_id = u.id
            WHERE lic.status = 'pending'
        """)
    
    @staticmethod
    def approve(claim_id, admin_id):
        execute_db("""
            UPDATE lost_item_claims 
            SET status = 'approved', 
                processed_by = ?, 
                processed_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, claim_id))
        
        claim = query_db("SELECT * FROM lost_item_claims WHERE id = ?", (claim_id,), one=True)
        if claim:
            execute_db("UPDATE lost_items SET status = 'claimed' WHERE id = ?", (claim['lost_item_id'],))
    
    @staticmethod
    def reject(claim_id, admin_id, notes):
        execute_db("""
            UPDATE lost_item_claims 
            SET status = 'rejected', 
                processed_by = ?, 
                processed_date = CURRENT_TIMESTAMP,
                admin_notes = ?
            WHERE id = ?
        """, (admin_id, notes, claim_id))

class FoundItemClaim:
    """Found item claim model"""
    
    @staticmethod
    def create(found_item_id, claimant_id):
        query = """
            INSERT INTO found_item_claims (found_item_id, claimant_id)
            VALUES (?, ?)
        """
        return execute_db(query, (found_item_id, claimant_id))
    
    @staticmethod
    def get_pending():
        return query_db("""
            SELECT fic.*, fi.item_name, fi.description, u.first_name, u.last_name, u.student_id
            FROM found_item_claims fic
            JOIN found_items fi ON fic.found_item_id = fi.id
            JOIN users u ON fic.claimant_id = u.id
            WHERE fic.status = 'pending'
        """)
    
    @staticmethod
    def approve(claim_id, admin_id):
        execute_db("""
            UPDATE found_item_claims 
            SET status = 'approved', 
                processed_by = ?, 
                processed_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, claim_id))
        
        claim = query_db("SELECT * FROM found_item_claims WHERE id = ?", (claim_id,), one=True)
        if claim:
            execute_db("UPDATE found_items SET status = 'claimed' WHERE id = ?", (claim['found_item_id'],))
    
    @staticmethod
    def reject(claim_id, admin_id, notes):
        execute_db("""
            UPDATE found_item_claims 
            SET status = 'rejected', 
                processed_by = ?, 
                processed_date = CURRENT_TIMESTAMP,
                admin_notes = ?
            WHERE id = ?
        """, (admin_id, notes, claim_id))

# ==================== Clubs Models ====================

class Club:
    """Club model"""
    
    @staticmethod
    def get_all():
        return query_db("SELECT * FROM clubs WHERE status = 'active' ORDER BY name")
    
    @staticmethod
    def get_pending():
        return query_db("SELECT * FROM clubs WHERE status = 'pending' ORDER BY created_at")
    
    @staticmethod
    def get_by_id(club_id):
        return query_db("SELECT * FROM clubs WHERE id = ?", (club_id,), one=True)
    
    @staticmethod
    def create(name, description, category, contact_email, dues_amount=0, created_by=None):
        query = """
            INSERT INTO clubs (name, description, category, contact_email, dues_amount, status, created_by)
            VALUES (?, ?, ?, ?, ?, 'pending', ?)
        """
        return execute_db(query, (name, description, category, contact_email, dues_amount, created_by))
    
    @staticmethod
    def approve(club_id, admin_id):
        execute_db("""
            UPDATE clubs 
            SET status = 'active', 
                approved_by = ?, 
                approved_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, club_id))
    
    @staticmethod
    def update(club_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        values.append(club_id)
        query = f"UPDATE clubs SET {', '.join(fields)} WHERE id = ?"
        execute_db(query, tuple(values))
    
    @staticmethod
    def delete(club_id):
        execute_db("DELETE FROM clubs WHERE id = ?", (club_id,))
    
    @staticmethod
    def get_members(club_id):
        return query_db("""
            SELECT cm.*, u.first_name, u.last_name, u.email, u.student_id
            FROM club_memberships cm
            JOIN users u ON cm.user_id = u.id
            WHERE cm.club_id = ? AND cm.status = 'active'
        """, (club_id,))
    
    @staticmethod
    def add_member(club_id, user_id, role='member'):
        existing = query_db(
            "SELECT * FROM club_memberships WHERE club_id = ? AND user_id = ?",
            (club_id, user_id),
            one=True
        )
        
        if existing:
            if existing['status'] == 'inactive':
                execute_db(
                    "UPDATE club_memberships SET status = 'active' WHERE id = ?",
                    (existing['id'],)
                )
                return existing['id']
            else:
                return existing['id']
        
        query = """
            INSERT INTO club_memberships (club_id, user_id, role, status)
            VALUES (?, ?, ?, 'pending')
        """
        return execute_db(query, (club_id, user_id, role))
    
    @staticmethod
    def approve_member(membership_id, admin_id):
        execute_db("""
            UPDATE club_memberships 
            SET status = 'active', 
                approved_by = ?, 
                approved_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, membership_id))
        
        membership = query_db("SELECT * FROM club_memberships WHERE id = ?", (membership_id,), one=True)
        if membership:
            execute_db(
                "UPDATE clubs SET members = members + 1 WHERE id = ?",
                (membership['club_id'],)
            )
    
    @staticmethod
    def remove_member(club_id, user_id):
        execute_db(
            "UPDATE club_memberships SET status = 'inactive' WHERE club_id = ? AND user_id = ?",
            (club_id, user_id)
        )
        execute_db(
            "UPDATE clubs SET members = members - 1 WHERE id = ?",
            (club_id,)
        )
    
    @staticmethod
    def pay_dues(club_id, user_id, amount):
        execute_db("""
            UPDATE club_memberships 
            SET dues_paid = 1, 
                dues_amount = ?, 
                dues_paid_date = CURRENT_TIMESTAMP 
            WHERE club_id = ? AND user_id = ?
        """, (amount, club_id, user_id))

class ClubMembership:  # This is the class we need - SINGULAR
    """Club membership model"""
    
    @staticmethod
    def get_user_memberships(user_id):
        return query_db("""
            SELECT cm.*, c.name as club_name, c.category
            FROM club_memberships cm
            JOIN clubs c ON cm.club_id = c.id
            WHERE cm.user_id = ? AND cm.status = 'active'
        """, (user_id,))
    
    @staticmethod
    def get_pending_requests():
        return query_db("""
            SELECT cm.*, c.name as club_name, u.first_name, u.last_name, u.student_id
            FROM club_memberships cm
            JOIN clubs c ON cm.club_id = c.id
            JOIN users u ON cm.user_id = u.id
            WHERE cm.status = 'pending'
        """)

class ClubEvent:
    """Club event model"""
    
    @staticmethod
    def get_upcoming():
        return query_db("""
            SELECT ce.*, c.name as club_name
            FROM club_events ce
            JOIN clubs c ON ce.club_id = c.id
            WHERE ce.event_date > datetime('now') AND ce.status = 'upcoming'
            ORDER BY ce.event_date
        """)
    
    @staticmethod
    def get_by_club(club_id):
        return query_db(
            "SELECT * FROM club_events WHERE club_id = ? ORDER BY event_date",
            (club_id,)
        )
    
    @staticmethod
    def create(club_id, title, description, event_date, location, max_participants, created_by):
        query = """
            INSERT INTO club_events (club_id, title, description, event_date, location, max_participants, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (club_id, title, description, event_date, location, max_participants, created_by))
    
    @staticmethod
    def approve(event_id, admin_id):
        execute_db("""
            UPDATE club_events 
            SET status = 'upcoming', 
                approved_by = ?, 
                approved_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, event_id))
    
    @staticmethod
    def rsvp(event_id, user_id):
        existing = query_db(
            "SELECT * FROM event_rsvps WHERE event_id = ? AND user_id = ?",
            (event_id, user_id),
            one=True
        )
        
        if existing:
            return existing['id']
        
        event = query_db("SELECT * FROM club_events WHERE id = ?", (event_id,), one=True)
        if event and event['max_participants'] and event['current_participants'] >= event['max_participants']:
            return False
        
        query = """
            INSERT INTO event_rsvps (event_id, user_id)
            VALUES (?, ?)
        """
        rsvp_id = execute_db(query, (event_id, user_id))
        
        execute_db(
            "UPDATE club_events SET current_participants = current_participants + 1 WHERE id = ?",
            (event_id,)
        )
        
        return rsvp_id
    
    @staticmethod
    def cancel_rsvp(event_id, user_id):
        execute_db(
            "DELETE FROM event_rsvps WHERE event_id = ? AND user_id = ?",
            (event_id, user_id)
        )
        execute_db(
            "UPDATE club_events SET current_participants = current_participants - 1 WHERE id = ?",
            (event_id,)
        )

# ==================== Medical Models ====================

class Doctor:
    """Doctor model"""
    
    @staticmethod
    def get_all():
        return query_db("SELECT * FROM doctors ORDER BY name")
    
    @staticmethod
    def get_available():
        return query_db("SELECT * FROM doctors WHERE available = 1 ORDER BY name")
    
    @staticmethod
    def get_by_id(doctor_id):
        return query_db("SELECT * FROM doctors WHERE id = ?", (doctor_id,), one=True)
    
    @staticmethod
    def create(name, specialty, email, phone, education, experience, languages, created_by=None):
        languages_json = json.dumps(languages) if languages else None
        query = """
            INSERT INTO doctors (name, specialty, email, phone, education, experience, languages, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (name, specialty, email, phone, education, experience, languages_json, created_by))
    
    @staticmethod
    def update(doctor_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                if key == 'languages' and isinstance(value, list):
                    value = json.dumps(value)
                fields.append(f"{key} = ?")
                values.append(value)
        values.append(doctor_id)
        values.append(datetime.datetime.now())
        query = f"UPDATE doctors SET {', '.join(fields)}, updated_at = ? WHERE id = ?"
        execute_db(query, tuple(values))
    
    @staticmethod
    def toggle_availability(doctor_id):
        doctor = Doctor.get_by_id(doctor_id)
        if doctor:
            new_status = 0 if doctor['available'] else 1
            execute_db("UPDATE doctors SET available = ? WHERE id = ?", (new_status, doctor_id))
            return new_status
        return None

class Appointment:
    """Appointment model"""
    
    @staticmethod
    def get_upcoming():
        return query_db("""
            SELECT a.*, u.first_name, u.last_name, u.student_id, d.name as doctor_name, d.specialty
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.status = 'upcoming' AND a.appointment_date >= date('now')
            ORDER BY a.appointment_date, a.appointment_time
        """)
    
    @staticmethod
    def get_user_appointments(user_id):
        return query_db("""
            SELECT a.*, d.name as doctor_name, d.specialty
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.user_id = ?
            ORDER BY a.appointment_date DESC
        """, (user_id,))
    
    @staticmethod
    def create(user_id, doctor_id, service_type, appointment_date, appointment_time, reason, created_by=None):
        query = """
            INSERT INTO appointments (user_id, doctor_id, service_type, appointment_date, appointment_time, reason, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (user_id, doctor_id, service_type, appointment_date, appointment_time, reason, created_by))
    
    @staticmethod
    def confirm(appointment_id, admin_id):
        execute_db("""
            UPDATE appointments 
            SET status = 'confirmed' 
            WHERE id = ?
        """, (appointment_id,))
    
    @staticmethod
    def cancel(appointment_id, admin_id, reason):
        execute_db("""
            UPDATE appointments 
            SET status = 'cancelled', 
                cancelled_by = ?, 
                cancelled_date = CURRENT_TIMESTAMP,
                cancellation_reason = ?
            WHERE id = ?
        """, (admin_id, reason, appointment_id))
    
    @staticmethod
    def complete(appointment_id):
        execute_db("UPDATE appointments SET status = 'completed' WHERE id = ?", (appointment_id,))

class Medication:
    """Medication model"""
    
    @staticmethod
    def get_all():
        return query_db("SELECT * FROM medications ORDER BY name")
    
    @staticmethod
    def get_available():
        return query_db("SELECT * FROM medications WHERE stock > 0 ORDER BY name")
    
    @staticmethod
    def get_by_id(medication_id):
        return query_db("SELECT * FROM medications WHERE id = ?", (medication_id,), one=True)
    
    @staticmethod
    def create(name, description, category, price, stock, requires_prescription, created_by=None):
        query = """
            INSERT INTO medications (name, description, category, price, stock, requires_prescription, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (name, description, category, price, stock, requires_prescription, created_by))
    
    @staticmethod
    def update(medication_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                fields.append(f"{key} = ?")
                values.append(value)
        values.append(medication_id)
        values.append(datetime.datetime.now())
        query = f"UPDATE medications SET {', '.join(fields)}, updated_at = ? WHERE id = ?"
        execute_db(query, tuple(values))
    
    @staticmethod
    def update_stock(medication_id, quantity):
        execute_db("UPDATE medications SET stock = stock + ? WHERE id = ?", (quantity, medication_id))

class Prescription:
    """Prescription model"""
    
    @staticmethod
    def get_user_prescriptions(user_id):
        return query_db("""
            SELECT p.*, d.name as doctor_name, m.name as medication_name, m.description as medication_description
            FROM prescriptions p
            JOIN doctors d ON p.doctor_id = d.id
            JOIN medications m ON p.medication_id = m.id
            WHERE p.user_id = ? AND p.status = 'active'
            ORDER BY p.expiry_date
        """, (user_id,))
    
    @staticmethod
    def create(user_id, doctor_id, medication_id, dosage, instructions, prescribed_date, expiry_date, refills, created_by=None):
        query = """
            INSERT INTO prescriptions (user_id, doctor_id, medication_id, dosage, instructions, prescribed_date, expiry_date, refills, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (user_id, doctor_id, medication_id, dosage, instructions, prescribed_date, expiry_date, refills, created_by))
    
    @staticmethod
    def request_refill(prescription_id):
        query = """
            INSERT INTO prescription_refills (prescription_id)
            VALUES (?)
        """
        return execute_db(query, (prescription_id,))
    
    @staticmethod
    def approve_refill(refill_id, admin_id):
        refill = query_db("SELECT * FROM prescription_refills WHERE id = ?", (refill_id,), one=True)
        if not refill:
            return False
        
        prescription = query_db("SELECT * FROM prescriptions WHERE id = ?", (refill['prescription_id'],), one=True)
        if not prescription or prescription['refills_used'] >= prescription['refills']:
            return False
        
        execute_db("""
            UPDATE prescription_refills 
            SET status = 'approved', 
                approved_by = ?, 
                approved_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (admin_id, refill_id))
        
        execute_db("""
            UPDATE prescriptions 
            SET refills_used = refills_used + 1 
            WHERE id = ?
        """, (prescription['id'],))
        
        return True

class MedicalRecord:
    """Medical record model"""
    
    @staticmethod
    def get_user_records(user_id):
        return query_db("""
            SELECT mr.*, d.name as doctor_name
            FROM medical_records mr
            JOIN doctors d ON mr.doctor_id = d.id
            WHERE mr.user_id = ?
            ORDER BY mr.record_date DESC
        """, (user_id,))
    
    @staticmethod
    def create(user_id, record_type, record_date, doctor_id, diagnosis, notes, created_by=None):
        query = """
            INSERT INTO medical_records (user_id, record_type, record_date, doctor_id, diagnosis, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return execute_db(query, (user_id, record_type, record_date, doctor_id, diagnosis, notes, created_by))

# ==================== Feedback Model ====================

class Feedback:
    """Feedback model"""
    
    @staticmethod
    def create(user_id, category, message):
        query = """
            INSERT INTO feedback (user_id, category, message)
            VALUES (?, ?, ?)
        """
        return execute_db(query, (user_id, category, message))
    
    @staticmethod
    def get_all():
        return query_db("""
            SELECT f.*, u.first_name, u.last_name, u.student_id, u.email
            FROM feedback f
            JOIN users u ON f.user_id = u.id
            ORDER BY f.submitted_date DESC
        """)
    
    @staticmethod
    def get_new():
        return query_db("""
            SELECT f.*, u.first_name, u.last_name, u.student_id, u.email
            FROM feedback f
            JOIN users u ON f.user_id = u.id
            WHERE f.status = 'new'
            ORDER BY f.submitted_date
        """)
    
    @staticmethod
    def respond(feedback_id, admin_id, response):
        execute_db("""
            UPDATE feedback 
            SET status = 'replied', 
                admin_response = ?, 
                responded_by = ?, 
                responded_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        """, (response, admin_id, feedback_id))