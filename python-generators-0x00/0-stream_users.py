#!/usr/bin/env python3
import psycopg2

def stream_users():
    try:
        connection = psycopg2.connect(
            dbname='ALX_prodev',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        cursor = connection.cursor(name='user_stream_cursor')  # Server-side cursor

        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        for row in cursor:
            yield {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }

        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Streaming error: {e}")
        return
