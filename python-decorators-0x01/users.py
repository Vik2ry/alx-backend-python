#!/usr/bin/env python3
"""
Initializes users.db with a sample users table and some data.
"""

import sqlite3

# Connect to or create users.db
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')

# Insert sample data
cursor.executemany('''
    INSERT INTO users (name, email) VALUES (?, ?)
''', [
    ('Alice Smith', 'alice@example.com'),
    ('Bob Johnson', 'bob@example.com'),
    ('Charlie Rose', 'charlie@example.com')
])

conn.commit()
conn.close()

print("✅ users.db initialized with sample data.")
