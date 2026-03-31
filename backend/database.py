import os
import sys
from supabase import create_client, Client
from .config import Config

SUPABASE_URL = Config.SUPABASE_URL
SUPABASE_KEY = Config.SUPABASE_KEY

# Initialize the Supabase client with error handling
try:
    if not SUPABASE_URL or not SUPABASE_KEY or "https" not in SUPABASE_URL:
        print(f"CRITICAL: Invalid Supabase configuration. URL: {SUPABASE_URL}")
        supabase = None
    else:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"CRITICAL: Failed to initialize Supabase client: {e}")
    supabase = None

def get_db():
    """Return the Supabase client"""
    if supabase is None:
        raise Exception("Supabase client not initialized. Check environment variables.")
    return supabase

def init_db():
    """
    Note: Supabase schema should be managed via the Supabase dashboard 
    or SQL editor using the provided schema.sql.
    """
    if supabase:
        print("Supabase client initialized.")
    else:
        print("Supabase client FAILED to initialize.")

def query_db(table, select="*", filters=None, one=False):
    """
    Perform a select query using Supabase SDK
    """
    db = get_db()
    query = db.table(table).select(select)
    
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
            
    result = query.execute()
    
    if one:
        return result.data[0] if result.data else None
    return result.data

def execute_db(table, data, operation='insert', filters=None):
    """
    Perform insert, update, or delete using Supabase SDK
    """
    db = get_db()
    if operation == 'insert':
        result = db.table(table).insert(data).execute()
        return result.data[0]['id'] if result.data else None
    
    elif operation == 'update':
        query = db.table(table).update(data)
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.data
    
    elif operation == 'delete':
        query = db.table(table).delete()
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.data

def close_db(e=None):
    """No specific close action needed for Supabase SDK"""
    pass
