#!/usr/bin/env python3
import psycopg2

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches"""
    try:
        connection = psycopg2.connect(
            dbname='ALX_prodev',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        cursor = connection.cursor(name='batch_cursor')
        cursor.itersize = batch_size
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        batch = []
        for row in cursor:
            batch.append({
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': row[3]
            })
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        print(f"Batch streaming error: {e}")
        return

def batch_processing(batch_size):
    """Processes batches and prints users over the age of 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
