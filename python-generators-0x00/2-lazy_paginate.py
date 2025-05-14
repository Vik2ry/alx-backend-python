#!/usr/bin/python3
import psycopg2

def paginate_users(page_size, offset):
    """Fetch a specific page of users from the DB using offset and limit"""
    try:
        connection = psycopg2.connect(
            dbname='ALX_prodev',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        cursor = connection.cursor()
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        rows = cursor.fetchall()
        connection.close()
        return [
            {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }
            for row in rows
        ]
    except psycopg2.Error as e:
        print(f"Pagination error: {e}")
        return []

def lazy_pagination(page_size):
    """Generator that lazily yields pages of users"""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
