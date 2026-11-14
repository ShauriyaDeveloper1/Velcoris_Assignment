"""
Query Management Demonstration Script
Loads environment settings via python-dotenv and displays all submitted enquiries stored in SQLite.
"""
import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

def main():
    # Load environment variables from .env
    base_dir = Path(__file__).resolve().parent
    env_file = base_dir / '.env'
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()

    raw_db_path = os.environ.get('DATABASE_PATH', 'instance/velcoris.db')
    db_path = Path(raw_db_path)
    if not db_path.is_absolute():
        db_path = (base_dir / db_path).resolve()

    print(f"Connecting to database at: {db_path}")
    if not db_path.exists():
        print("Database file does not exist yet. Please submit an enquiry on the website first.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM enquiries ORDER BY id ASC")
        rows = cursor.fetchall()
        print(f"\nFound {len(rows)} enquiry record(s):\n" + "="*85)
        for row in rows:
            print(f"ID          : #{row['id']}")
            print(f"Created At  : {row['created_at']} UTC")
            print(f"Status      : {row['status']}")
            print(f"Name        : {row['name']}")
            print(f"Email       : {row['email']}")
            print(f"Organisation: {row['organisation'] or 'N/A'}")
            print(f"Type        : {row['enquiry_type']}")
            print(f"Subject     : {row['subject']}")
            print(f"Message     : {row['message']}")
            print("-" * 85)
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    main()

