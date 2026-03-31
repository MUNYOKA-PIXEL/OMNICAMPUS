import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

def test_connection():
    try:
        print(f"Connecting to: {DATABASE_URL}")
        conn = psycopg2.connect(DATABASE_URL)
        print("Successfully connected to Supabase PostgreSQL!")
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f"You are connected to - {record}")
        
        # Initialize schema
        schema_path = os.path.join('OMNICAMPUS', 'database', 'schema.sql')
        if not os.path.exists(schema_path):
            schema_path = os.path.join('database', 'schema.sql')
            
        print(f"Reading schema from: {schema_path}")
        with open(schema_path, 'r') as f:
            schema = f.read()
            
        # Refined PostgreSQL conversion
        schema = schema.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        # PostgreSQL doesn't like quotes in some cases for DEFAULT, but for timestamps it's fine
        # Ensure we don't have multiple conflicting replacements
        
        print("Executing schema...")
        cur.execute(schema)
        conn.commit()
        print("Database schema initialized successfully!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_connection()
