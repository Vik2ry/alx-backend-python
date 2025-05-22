#!/usr/bin/env python3
"""
Decorator to automatically handle SQLite DB connections.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that opens a DB connection, passes it to the function,
    and ensures it's closed after the function completes.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open connection to users.db
        conn = sqlite3.connect('users.db')
        try:
            # Pass connection as first argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
