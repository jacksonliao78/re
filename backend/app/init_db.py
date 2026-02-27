
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import init_db, engine, Base
from app.db.models import User, IgnoredJob  # noqa: F401 - register tables with Base  

def main():
    
    db_url = os.environ.get('DATABASE_URL', 'Using default')
    if db_url.startswith('postgresql://'):
        if '@' in db_url:
            parts = db_url.split('@')
            if ':' in parts[0] and parts[0].count(':') >= 2:
                user_pass = parts[0].split('://')[1]
                if ':' in user_pass:
                    user = user_pass.split(':')[0]
                    db_url_display = f"postgresql://{user}:***@{parts[1]}"
                else:
                    db_url_display = db_url
            else:
                db_url_display = db_url
        else:
            db_url_display = db_url
    else:
        db_url_display = db_url
    
    print(f"Database URL: {db_url_display}")
    
    try:
        # This creates all tables defined in models that inherit from Base
        init_db()
        # Add new columns to existing users table if present (idempotent)
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS default_resume JSONB"))
            conn.commit()
        print("Database tables created successfully")
        
        # Verify by listing tables
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if tables:
            print(f"\nCreated tables: {', '.join(tables)}")
            
            # Show table structure for users table
            if 'users' in tables:
                columns = inspector.get_columns('users')
                print(f"\nUsers table structure:")
                for col in columns:
                    print(f"  - {col['name']}: {col['type']}")
        else:
            print("\n No tables found ")
            
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
    
        sys.exit(1)

if __name__ == "__main__":
    main()
