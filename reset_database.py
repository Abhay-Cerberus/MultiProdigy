import os
import sqlite3

def reset_database():
    """Reset the database by removing and recreating it"""
    db_path = "multiprodigy_logs.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Removed existing database: {db_path}")
    
    # The new database will be created automatically when the log collector starts
    print("✅ Database will be recreated with correct schema on next startup")

if __name__ == "__main__":
    reset_database()