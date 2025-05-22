import sqlite3
from typing import List, Tuple

def create_sample_database() -> None:
    """
    Creates a SQLite database with a users table and sample data.
    """
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        ''')
        sample_users: List[Tuple[str, str]] = [
            ('Alice Smith', 'alice.smith@example.com'),
            ('Bob Johnson', 'bob.johnson@example.com'),
            ('Charlie Brown', 'charlie.brown@example.com')
        ]
        cursor.executemany('INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)', sample_users)
        conn.commit()
        print("Sample database created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    create_sample_database()
