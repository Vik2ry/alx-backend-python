#!/usr/bin/env python3
"""
Decorator to cache query results to avoid redundant DB calls.
"""

import time
import sqlite3
import functools

query_cache = {}


def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the function,
    and ensures it is closed after execution.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    """
    Caches query results based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Try to get query from kwargs or args
        query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else None)

        if query in query_cache:
            print("[CACHE HIT] Returning cached result.")
            return query_cache[query]

        print("[CACHE MISS] Executing and caching query.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Demonstrate caching behavior
if __name__ == "__main__":
    print("[CALL 1] Fetching users (should execute query)")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    print("\n[CALL 2] Fetching users again (should use cache)")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
