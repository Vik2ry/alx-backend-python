import sqlite3
import functools
#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""

def log_queries():
    """
    Decorator to log SQL queries executed by the decorated function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Attempt to extract the SQL query argument
            query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else "UNKNOWN QUERY")
            print(f"[LOG] Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
