import sqlite3
import os
from contextlib import contextmanager
from flask import current_app, g

DATABASE_PATH = 'database/omnicampus.db'

def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database with schema"""
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
    
    with get_db_connection() as conn:
        conn.executescript(schema)
    
    print("Database initialized successfully")

def query_db(query, args=(), one=False):
    """Execute a query and return results"""
    with get_db_connection() as conn:
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Execute a query that modifies data"""
    with get_db_connection() as conn:
        cur = conn.execute(query, args)
        conn.commit()
        return cur.lastrowid

def close_db(e=None):
    """Close database connection"""
    db = g.pop('_database', None)
    if db is not None:
        db.close()