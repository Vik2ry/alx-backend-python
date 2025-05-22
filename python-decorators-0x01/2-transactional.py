#!/usr/bin/env python3
"""
Decorator that ensures a database operation is executed within a transaction.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Opens a connection to 'users.db' and passes it to the wrapped function.
    Closes the connection after execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """
    Wraps a DB function in a transaction.
    Commits if successful, rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Transaction failed, rolled back: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Run the update with automatic transaction management
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("User email updated.")
