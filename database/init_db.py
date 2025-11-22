import sqlite3
import os

DATABASE_PATH = "tasks.db"


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_database():
    """Initialize database and create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'medium',
            due_date DATE,
            created_at TEXT,
            updated_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")


# Run this when module is imported
init_database()