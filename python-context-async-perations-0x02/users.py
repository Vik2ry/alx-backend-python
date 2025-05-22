import importlib
import sqlite3


import sqlite3

def setup_new_users_table(db_path="test.db"):
    users_data = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 20),
        ("Carol", "carol@example.com", 27),
        ("Dave", "dave@example.com", 24),
        ("Eve", "eve@example.com", 35),
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Rename old users table to users_backup if exists
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='users'
    """)
    if cursor.fetchone():
        cursor.execute("ALTER TABLE users RENAME TO users_backup")
        print("Renamed existing 'users' table to 'users_backup'")

    # Create new users table
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert all given users
    cursor.executemany(
        "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
        users_data
    )
    conn.commit()
    print(f"Created new 'users' table and inserted {len(users_data)} records.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    setup_new_users_table()  # Create DB and insert data if needed

    databaseConnection = importlib.import_module('0-databaseconnection')
    DatabaseConnection = databaseConnection.DatabaseConnection  # Import your class here

    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)