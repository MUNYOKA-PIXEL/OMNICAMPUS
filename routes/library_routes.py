from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from backend.models import LibraryBook, BookLoan, User
from backend.auth import token_required, admin_required

bp = Blueprint('library', __name__)

@bp.route('/books', methods=['GET'])
def get_books():
    """Get all library books"""
    books = LibraryBook.get_all()
    return jsonify([dict(book) for book in books])

@bp.route('/books/search', methods=['GET'])
def search_books():
    """Search books by title, author, or ISBN"""
    query = request.args.get('q', '')
    books = LibraryBook.search(query)
    return jsonify([dict(book) for book in books])

@bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get book by ID"""
    book = LibraryBook.get_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(dict(book))

@bp.route('/books', methods=['POST'])
@admin_required
def add_book(current_user):
    """Add a new book (admin only)"""
    data = request.json
    
    required_fields = ['title', 'author', 'total_copies']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    book_id = LibraryBook.create(
        title=data['title'],
        author=data['author'],
        isbn=data.get('isbn', ''),
        category=data.get('category', 'General'),
        total_copies=data['total_copies']
    )
    
    return jsonify({'id': book_id, 'message': 'Book added successfully'}), 201

@bp.route('/books/<int:book_id>', methods=['PUT'])
@admin_required
def update_book(current_user, book_id):
    """Update book details (admin only)"""
    data = request.json
    LibraryBook.update(book_id, **data)
    return jsonify({'message': 'Book updated successfully'})

@bp.route('/books/<int:book_id>', methods=['DELETE'])
@admin_required
def delete_book(current_user, book_id):
    """Delete a book (admin only)"""
    LibraryBook.delete(book_id)
    return jsonify({'message': 'Book deleted successfully'})

@bp.route('/loans', methods=['GET'])
@admin_required
def get_all_loans(current_user):
    """Get all current loans (admin only)"""
    loans = BookLoan.get_current_loans()
    return jsonify([dict(loan) for loan in loans])

@bp.route('/loans/user', methods=['GET'])
@token_required
def get_user_loans(current_user):
    """Get loans for current user"""
    loans = BookLoan.get_user_loans(current_user['id'])
    return jsonify([dict(loan) for loan in loans])

@bp.route('/loans', methods=['POST'])
@admin_required
def issue_book(current_user):
    """Issue a book to a student (admin only)"""
    data = request.json
    
    required_fields = ['user_id', 'book_id', 'due_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
    
    loan_id = BookLoan.issue_book(
        user_id=data['user_id'],
        book_id=data['book_id'],
        due_date=data['due_date']
    )
    
    if not loan_id:
        return jsonify({'error': 'Book not available'}), 400
    
    return jsonify({'id': loan_id, 'message': 'Book issued successfully'})

@bp.route('/loans/<int:loan_id>/return', methods=['POST'])
@admin_required
def return_book(current_user, loan_id):
    """Return a book (admin only)"""
    success = BookLoan.return_book(loan_id)
    
    if not success:
        return jsonify({'error': 'Loan not found or already returned'}), 400
    
    return jsonify({'message': 'Book returned successfully'})

@bp.route('/loans/calculate-fines', methods=['POST'])
@admin_required
def calculate_fines(current_user):
    """Calculate fines for overdue books (admin only)"""
    BookLoan.calculate_fines()
    return jsonify({'message': 'Fines calculated successfully'})
