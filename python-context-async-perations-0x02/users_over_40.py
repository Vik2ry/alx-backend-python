import sqlite3

def insert_users_over_40(db_path="test.db"):
    new_users = [
        ("Frank", "frank@example.com", 45),
        ("Grace", "grace@example.com", 52),
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for user in new_users:
        try:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                user
            )
            print(f"Inserted user: {user}")
        except sqlite3.IntegrityError:
            print(f"User already exists or duplicate email: {user[1]}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    insert_users_over_40()
