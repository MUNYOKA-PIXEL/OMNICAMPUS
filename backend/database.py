import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_db():
    """Return the Supabase client"""
    return supabase

def init_db():
    """
    Note: Supabase schema should be managed via the Supabase dashboard 
    or SQL editor using the provided schema.sql.
    """
    print("Supabase client initialized. Please ensure schema is applied in Supabase SQL Editor.")

def query_db(table, select="*", filters=None, one=False):
    """
    Perform a select query using Supabase SDK
    Example: query_db('users', filters={'email': 'test@test.com'}, one=True)
    """
    query = supabase.table(table).select(select)
    
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
    if operation == 'insert':
        result = supabase.table(table).insert(data).execute()
        return result.data[0]['id'] if result.data else None
    
    elif operation == 'update':
        query = supabase.table(table).update(data)
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.data
    
    elif operation == 'delete':
        query = supabase.table(table).delete()
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        result = query.execute()
        return result.data

def close_db(e=None):
    """No specific close action needed for Supabase SDK"""
    pass
