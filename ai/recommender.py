"""
OmniCampus AI Recommendation System
- Book recommendations based on borrowing history
- Simple collaborative filtering
- Campus assistant chatbot
"""

import sqlite3
import numpy as np
from collections import Counter
import json
import os
from datetime import datetime, timedelta

class BookRecommender:
    """AI-powered book recommendation engine"""
    
    def __init__(self, db_path='database/omnicampus.db'):
        self.db_path = db_path
        self.conn = None
        self.connect()
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(f"Database connection error: {e}")
            self.conn = None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def get_user_borrowing_history(self, user_id):
        """Get borrowing history for a user"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT bl.*, lb.title, lb.author, lb.category, lb.id as book_id
            FROM book_loans bl
            JOIN library_books lb ON bl.book_id = lb.id
            WHERE bl.user_id = ?
            ORDER BY bl.issue_date DESC
        """, (user_id,))
        return cursor.fetchall()
    
    def get_all_borrowing_data(self):
        """Get all borrowing data for collaborative filtering"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT bl.user_id, lb.id as book_id, lb.title, lb.author, lb.category
            FROM book_loans bl
            JOIN library_books lb ON bl.book_id = lb.id
        """)
        return cursor.fetchall()
    
    def get_all_books(self):
        """Get all books in library"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT * FROM library_books
            WHERE available_copies > 0
            ORDER BY title
        """)
        return cursor.fetchall()
    
    def get_popular_books(self, limit=5):
        """Get most popular books overall"""
        if not self.conn:
            return self._get_mock_popular_books()
        
        try:
            cursor = self.conn.execute("""
                SELECT lb.*, COUNT(bl.id) as borrow_count
                FROM library_books lb
                LEFT JOIN book_loans bl ON lb.id = bl.book_id
                GROUP BY lb.id
                ORDER BY borrow_count DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()
        except:
            return self._get_mock_popular_books()
    
    def _get_mock_popular_books(self):
        """Return mock popular books for demo"""
        return [
            {'id': 1, 'title': 'Clean Code', 'author': 'Robert C. Martin', 'category': 'Programming', 'available_copies': 3},
            {'id': 2, 'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'category': 'Computer Science', 'available_copies': 2},
            {'id': 3, 'title': 'The Pragmatic Programmer', 'author': 'David Thomas', 'category': 'Programming', 'available_copies': 4},
            {'id': 4, 'title': 'Design Patterns', 'author': 'Erich Gamma', 'category': 'Software Engineering', 'available_copies': 1},
            {'id': 5, 'title': 'Database System Concepts', 'author': 'Abraham Silberschatz', 'category': 'Computer Science', 'available_copies': 3}
        ]
    
    def recommend_by_category(self, user_id, limit=5):
        """Recommend books based on user's preferred categories"""
        history = self.get_user_borrowing_history(user_id)
        
        if not history or len(history) == 0:
            # New user - recommend popular books
            return self.get_popular_books(limit)
        
        # Count categories from borrowing history
        categories = [book['category'] for book in history if book['category']]
        if not categories:
            return self.get_popular_books(limit)
        
        # Find most borrowed category
        category_counts = Counter(categories)
        top_category = category_counts.most_common(1)[0][0]
        
        # Get books in top category that user hasn't borrowed
        borrowed_book_ids = [book['book_id'] for book in history]
        
        if not self.conn:
            # Return mock recommendations
            return [b for b in self._get_mock_popular_books() if b['category'] == top_category][:limit]
        
        try:
            placeholders = ','.join('?' * len(borrowed_book_ids)) if borrowed_book_ids else 'NULL'
            cursor = self.conn.execute(f"""
                SELECT * FROM library_books 
                WHERE category = ? AND id NOT IN ({placeholders})
                AND available_copies > 0
                ORDER BY title
                LIMIT ?
            """, [top_category] + (borrowed_book_ids if borrowed_book_ids else []) + [limit])
            return cursor.fetchall()
        except:
            return self._get_mock_popular_books()[:limit]
    
    def recommend_collaborative(self, user_id, limit=5):
        """Simple collaborative filtering based on other users with similar borrowing patterns"""
        all_loans = self.get_all_borrowing_data()
        user_loans = [loan for loan in all_loans if loan['user_id'] == user_id]
        
        if not user_loans or len(user_loans) < 2:
            return self.recommend_by_category(user_id, limit)
        
        # Find users who borrowed similar books
        user_book_ids = set([loan['book_id'] for loan in user_loans])
        
        similar_users = []
        for loan in all_loans:
            if loan['user_id'] != user_id and loan['book_id'] in user_book_ids:
                similar_users.append(loan['user_id'])
        
        if not similar_users:
            return self.recommend_by_category(user_id, limit)
        
        # Find most popular books among similar users
        popular_books = Counter()
        for loan in all_loans:
            if loan['user_id'] in similar_users and loan['book_id'] not in user_book_ids:
                popular_books[loan['book_id']] += 1
        
        if not popular_books:
            return self.recommend_by_category(user_id, limit)
        
        # Get top recommended books
        top_book_ids = [book_id for book_id, count in popular_books.most_common(limit)]
        
        if not self.conn:
            return self._get_mock_popular_books()[:limit]
        
        try:
            cursor = self.conn.execute(
                "SELECT * FROM library_books WHERE id IN ({})".format(','.join('?' * len(top_book_ids))),
                top_book_ids
            )
            return cursor.fetchall()
        except:
            return self._get_mock_popular_books()[:limit]
    
    def get_recommendations(self, user_id, limit=5):
        """Get personalized book recommendations"""
        # Try collaborative filtering first
        recommendations = self.recommend_collaborative(user_id, limit)
        
        # If not enough, fall back to category-based
        if len(recommendations) < limit:
            category_recs = self.recommend_by_category(user_id, limit - len(recommendations))
            # Combine without duplicates
            rec_ids = set([r['id'] for r in recommendations])
            for rec in category_recs:
                if rec['id'] not in rec_ids:
                    recommendations.append(rec)
                    rec_ids.add(rec['id'])
        
        return recommendations
    
    def search_with_ai(self, query):
        """Enhanced search with AI suggestions"""
        # Basic search
        search_term = f"%{query}%"
        
        if not self.conn:
            # Return mock search results
            books = self._get_mock_popular_books()
            return [b for b in books if query.lower() in b['title'].lower() or 
                    query.lower() in b['author'].lower()][:10]
        
        try:
            cursor = self.conn.execute("""
                SELECT * FROM library_books 
                WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR category LIKE ?
                AND available_copies > 0
            """, (search_term, search_term, search_term, search_term))
            
            results = cursor.fetchall()
            
            # If no results, suggest related terms
            if len(results) == 0:
                # Simple keyword matching
                keywords = query.lower().split()
                suggestions = []
                
                all_books = self.get_all_books()
                for book in all_books:
                    book_text = f"{book['title']} {book['author']} {book['category']}".lower()
                    score = sum(1 for keyword in keywords if keyword in book_text)
                    if score > 0:
                        suggestions.append({
                            'book': dict(book),
                            'score': score / len(keywords)
                        })
                
                suggestions.sort(key=lambda x: x['score'], reverse=True)
                return [s['book'] for s in suggestions[:10]]
            
            return [dict(row) for row in results]
        except:
            return self._get_mock_popular_books()
    
    def get_trending_topics(self):
        """Get trending book categories/topics"""
        if not self.conn:
            return [
                {'category': 'Programming', 'borrow_count': 45},
                {'category': 'Computer Science', 'borrow_count': 38},
                {'category': 'Data Science', 'borrow_count': 27},
                {'category': 'Web Development', 'borrow_count': 22},
                {'category': 'Machine Learning', 'borrow_count': 18}
            ]
        
        try:
            cursor = self.conn.execute("""
                SELECT lb.category, COUNT(bl.id) as borrow_count
                FROM book_loans bl
                JOIN library_books lb ON bl.book_id = lb.id
                WHERE bl.issue_date > datetime('now', '-30 days')
                GROUP BY lb.category
                ORDER BY borrow_count DESC
                LIMIT 5
            """)
            return cursor.fetchall()
        except:
            return []

class CampusAssistant:
    """Simple rule-based chatbot for campus queries"""
    
    def __init__(self):
        self.responses = {
            'library': [
                "📚 The library is open Monday-Friday 8am-8pm, Saturday 9am-5pm.",
                "📖 You can borrow up to 5 books for 14 days.",
                "💰 Late fees are KES 50 per day for overdue books.",
                "🔍 Use the search feature in the Library section to find books.",
                "📱 You can renew books online through your dashboard."
            ],
            'club': [
                "🎯 There are several active clubs including DevClub, Business Club, and AI/ML Society.",
                "👥 You can join clubs from the Clubs section in your dashboard.",
                "📅 Club events are listed in the dashboard and clubs pages.",
                "💰 Club dues vary by club - check individual club pages for details.",
                "🎉 Joining clubs is a great way to meet people and build your network!"
            ],
            'lost': [
                "🔍 Report lost items in the Lost & Found section immediately.",
                "✅ Check the 'Potential Matches' tab to see if your item has been found.",
                "📸 Include detailed descriptions and photos when reporting.",
                "⏰ Items are kept for 30 days before being donated.",
                "📞 You can claim found items by contacting the admin."
            ],
            'fine': [
                "💰 Library fines are KES 50 per day for overdue books.",
                "💳 You can pay fines online via M-Pesa in the Library section.",
                "📊 Check your dashboard for outstanding fines and due dates.",
                "⚠️ Unpaid fines may affect your graduation clearance.",
                "🔄 Club dues are separate from library fines."
            ],
            'book': [
                "📚 You can search for books in the Library section.",
                "🔍 Use the search bar to find books by title, author, or ISBN.",
                "📖 Check book availability before visiting the library.",
                "⭐ Get personalized book recommendations in your dashboard.",
                "📱 Request books that aren't available in the library."
            ],
            'event': [
                "📅 Upcoming events are displayed on your dashboard.",
                "🎯 Join clubs to see their exclusive events.",
                "✅ RSVP to events to save your spot.",
                "📧 Event reminders are sent to your email.",
                "🎉 Club events are a great way to get involved!"
            ],
            'help': [
                "🤖 I'm your campus assistant! I can help with:\n" +
                "• Library hours and book loans\n" +
                "• Club information and events\n" +
                "• Lost & Found reporting\n" +
                "• Fine payments and dues\n" +
                "• Book recommendations",
                "💡 Try asking me about: library, clubs, lost items, fines, books, events",
                "📱 You can also check your dashboard for personalized information."
            ],
            'default': [
                "🤔 I'm not sure about that. Try asking about:\n" +
                "• Library hours and policies\n" +
                "• Student clubs and events\n" +
                "• Lost & Found reporting\n" +
                "• Fines and payments\n" +
                "• Book recommendations",
                "💡 For specific questions, try using keywords like 'library', 'club', 'lost', 'fine', or 'book'."
            ]
        }
    
    def get_response(self, query):
        """Get response based on query keywords"""
        if not query:
            return "Please ask me something!"
        
        query = query.lower()
        
        # Check for multiple keywords
        if 'library' in query or 'book' in query or 'borrow' in query:
            return np.random.choice(self.responses['library'])
        elif 'club' in query or 'society' in query:
            return np.random.choice(self.responses['club'])
        elif 'lost' in query or 'found' in query:
            return np.random.choice(self.responses['lost'])
        elif 'fine' in query or 'fee' in query or 'pay' in query:
            return np.random.choice(self.responses['fine'])
        elif 'help' in query or 'what' in query or 'how' in query:
            return np.random.choice(self.responses['help'])
        elif 'event' in query:
            return np.random.choice(self.responses['event'])
        else:
            return np.random.choice(self.responses['default'])
    
    def suggest_books(self, interest):
        """Suggest books based on interest"""
        interest = interest.lower()
        
        book_map = {
            'programming': ['Clean Code', 'The Pragmatic Programmer', 'Code Complete'],
            'python': ['Python Crash Course', 'Fluent Python', 'Automate the Boring Stuff'],
            'web': ['HTML and CSS', 'JavaScript: The Good Parts', 'Eloquent JavaScript'],
            'data': ['Python for Data Analysis', 'Storytelling with Data', 'Data Science for Business'],
            'ai': ['Artificial Intelligence: A Modern Approach', 'Pattern Recognition', 'Deep Learning'],
            'business': ['Zero to One', 'The Lean Startup', 'Good to Great'],
            'database': ['Database System Concepts', 'SQL for Data Analysis', 'Designing Data-Intensive Applications'],
            'algorithms': ['Introduction to Algorithms', 'Algorithm Design Manual', 'Grokking Algorithms']
        }
        
        for key, books in book_map.items():
            if key in interest:
                return f"📚 Based on your interest in {interest}, I recommend:\n" + "\n".join([f"• {book}" for book in books[:3]])
        
        return "💡 I can suggest books if you tell me what you're interested in (programming, python, web, data, AI, business, etc.)"
    
    def get_faq(self, topic=None):
        """Get FAQ responses"""
        faqs = {
            'library_hours': "The library is open Monday-Friday 8am-8pm, Saturday 9am-5pm, and closed Sunday.",
            'borrow_limit': "Students can borrow up to 5 books for 14 days.",
            'fine_rate': "Late fees are KES 50 per day for overdue books.",
            'club_list': "Active clubs include DevClub, Business Club, AI/ML Society, Robotics Club, and Debate Society.",
            'lost_procedure': "Report lost items in the Lost & Found section. Check for matches regularly.",
            'payment': "Pay fines and dues online via M-Pesa in the respective sections."
        }
        
        if topic and topic in faqs:
            return faqs[topic]
        
        return "What would you like to know about?"