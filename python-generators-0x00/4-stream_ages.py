#!/usr/bin/python3
import psycopg2

def stream_user_ages():
    """Generator that yields user ages one by one"""
    try:
        connection = psycopg2.connect(
            dbname='ALX_prodev',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for row in cursor:
            yield row[0]

        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        print(f"Streaming error: {e}")

def calculate_average_age():
    """Calculates the average age using a generator"""
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total_age / count:.2f}")
    else:
        print("No users found.")
