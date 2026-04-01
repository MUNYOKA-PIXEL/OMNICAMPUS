import os
import sys
from supabase import create_client, Client, ClientOptions
from config import Config

SUPABASE_URL = Config.SUPABASE_URL
SUPABASE_KEY = Config.SUPABASE_KEY

# Initialize the Supabase client
try:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print(f"CRITICAL: Missing Supabase configuration.")
        supabase = None
    else:
        # Use ClientOptions for v2.x
        options = ClientOptions(postgrest_client_timeout=10)
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY, options=options)
except Exception as e:
    print(f"CRITICAL: Failed to initialize Supabase client: {e}")
    supabase = None

def get_db():
    """Return the Supabase client"""
    if supabase is None:
        raise Exception("Supabase client not initialized. Check environment variables.")
    return supabase

def init_db():
    if supabase:
        print("Supabase client initialized.")
    else:
        print("Supabase client FAILED to initialize.")

def query_db(table, select="*", filters=None, one=False):
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
    pass
