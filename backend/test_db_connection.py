"""
Test script to verify database connection and schema setup.
Run this to ensure your RDS MySQL database is properly configured.

From project root:
  python -m backend.test_db_connection
  or
  cd backend && python test_db_connection.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

try:
    from .config import config
except ImportError:
    from config import config

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection and verify tables exist."""
    
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    # Get configuration - check if DATABASE_URL is in environment first
    env_database_url = os.getenv('DATABASE_URL')
    if env_database_url:
        database_url = env_database_url
        # Add charset if not present (for MySQL)
        if 'mysql' in database_url and 'charset' not in database_url:
            separator = '&' if '?' in database_url else '?'
            database_url = f"{database_url}{separator}charset=utf8mb4"
    else:
        # Fall back to config
        app_config = config.get(os.getenv('FLASK_ENV', 'production'))
        database_url = app_config.SQLALCHEMY_DATABASE_URI
    
    # Mask password in output
    safe_url = database_url
    if '@' in safe_url:
        parts = safe_url.split('@')
        if ':' in parts[0]:
            user_pass = parts[0].split(':')
            if len(user_pass) == 2:
                safe_url = f"{user_pass[0]}:****@{parts[1]}"
    
    print(f"\nDatabase URL: {safe_url}")
    print(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    
    try:
        # Create engine
        print("\n1. Creating database engine...")
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        print("2. Testing connection...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"   ✓ Connected successfully!")
            print(f"   MySQL Version: {version}")
            
            # Check database name
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            print(f"   Current Database: {db_name}")
        
        # Check tables
        print("\n3. Checking tables...")
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = [
            'job_descriptions',
            'interviews',
            'interview_questions',
            'question_cache',
            'generation_logs'
        ]
        
        print(f"   Found {len(tables)} table(s):")
        for table in tables:
            marker = "✓" if table in expected_tables else "?"
            print(f"   {marker} {table}")
        
        # Verify all expected tables exist
        missing_tables = [t for t in expected_tables if t not in tables]
        if missing_tables:
            print(f"\n   ⚠ Warning: Missing tables: {', '.join(missing_tables)}")
        else:
            print(f"\n   ✓ All expected tables found!")
        
        # Check table structure
        print("\n4. Verifying table structure...")
        for table in expected_tables:
            if table in tables:
                columns = inspector.get_columns(table)
                print(f"   {table}: {len(columns)} columns")
                
                # Check for JSON columns
                json_cols = [col['name'] for col in columns if 'json' in str(col['type']).lower()]
                if json_cols:
                    print(f"      JSON columns: {', '.join(json_cols)}")
        
        # Check indexes
        print("\n5. Checking indexes...")
        total_indexes = 0
        for table in expected_tables:
            if table in tables:
                indexes = inspector.get_indexes(table)
                total_indexes += len(indexes)
                if indexes:
                    print(f"   {table}: {len(indexes)} index(es)")
        
        print(f"\n   ✓ Total indexes: {total_indexes}")
        
        # Check foreign keys
        print("\n6. Checking foreign keys...")
        fk_count = 0
        for table in expected_tables:
            if table in tables:
                fks = inspector.get_foreign_keys(table)
                fk_count += len(fks)
                if fks:
                    for fk in fks:
                        print(f"   {table}.{fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        print(f"\n   ✓ Total foreign keys: {fk_count}")
        
        # Test charset/collation
        print("\n7. Verifying charset and collation...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT TABLE_NAME, TABLE_COLLATION 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME IN ('job_descriptions', 'interviews', 'interview_questions', 'question_cache', 'generation_logs')
                ORDER BY TABLE_NAME
            """))
            rows = result.fetchall()
            for row in rows:
                collation = row[1]
                status = "✓" if 'utf8mb4' in collation else "⚠"
                print(f"   {status} {row[0]}: {collation}")
        
        print("\n" + "=" * 60)
        print("✓ Database connection test completed successfully!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\nX Error connecting to database:")
        print(f"  {type(e).__name__}: {str(e)}")
        print("\n" + "=" * 60)
        print("Troubleshooting:")
        print("1. Check that your .env file has the correct DATABASE_URL")
        print("2. Verify your RDS MySQL instance is accessible")
        print("3. Check security group settings allow your IP")
        print("4. Verify username and password are correct")
        print("=" * 60)
        return False

if __name__ == '__main__':
    test_connection()
