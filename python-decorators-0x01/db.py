import sqlite3

from datetime import datetime

# Connect to DB
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Insert a user
cursor.execute('''
    INSERT INTO users (username, email, password, created_at)
    VALUES (?, ?, ?, ?)
''', (
    'chris_user',
    'chris@example.com',
    'supersecret123',  # Normally you'd hash this!
    datetime.now().isoformat()
))

conn.commit()
conn.close()
