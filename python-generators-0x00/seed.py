#!/usr/bin/env python3
import psycopg2
import csv
import uuid
import time

def connect_db():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='db',
            port='5432'
        )
        return connection
    except psycopg2.Error as e:
        print(f"Connection error: {e}")
        return None

def create_database(connection):
    try:
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'ALX_prodev'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE "ALX_prodev"')
            print("Database ALX_prodev created successfully")
        cursor.close()
    except psycopg2.Error as e:
        print(f"Database creation error: {e}")

def connect_to_prodev(retries=5, delay=2):
    for i in range(retries):
        try:
            connection = psycopg2.connect(
                dbname='ALX_prodev',
                user='postgres',
                password='postgres',
                host='db',
                port='5432'
            )
            return connection
        except psycopg2.Error as e:
            print(f"Attempt {i+1}: Connection to ALX_prodev failed: {e}")
            time.sleep(delay)
    print("Failed to connect to ALX_prodev after multiple attempts.")
    return None


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except psycopg2.Error as e:
        print(f"Table creation error: {e}")

def insert_data(connection, filename):
    try:
        cursor = connection.cursor()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row.get('user_id') or str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id) DO NOTHING
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Data insertion error: {e}")
