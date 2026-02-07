import sqlite3
import os
from datetime import datetime

# ---------------- DATABASE PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cartoon_app.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TEXT,
        last_login TEXT
    )
    """)

    # TRANSACTIONS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        payment_status TEXT,
        transaction_date TEXT,
        payment_method TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    """)

    # IMAGE HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ImageHistory (
        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        original_image_path TEXT,
        processed_image_path TEXT,
        style_applied TEXT,
        processing_date TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ All tables created successfully!")


# ---------------- INSERT SAMPLE DATA ----------------
def insert_sample_user():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO Users
    (username, email, password, created_at)
    VALUES (?, ?, ?, ?)
    """, (
        "testuser",
        "testuser@gmail.com",
        "hashed_password_123",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()
    print("✅ Sample user inserted")


def insert_sample_transaction():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Transactions
    (user_id, amount, payment_status, transaction_date, payment_method)
    VALUES (?, ?, ?, ?, ?)
    """, (
        1,
        99.99,
        "SUCCESS",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "UPI"
    ))

    conn.commit()
    conn.close()
    print("✅ Sample transaction inserted")


def insert_sample_image():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ImageHistory
    (user_id, original_image_path, processed_image_path, style_applied, processing_date)
    VALUES (?, ?, ?, ?, ?)
    """, (
        1,
        "uploads/original.jpg",
        "outputs/cartoon.jpg",
        "Cartoon",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()
    print("✅ Sample image history inserted")


# ---------------- FETCH DATA (OPTIONAL TEST) ----------------
def fetch_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    return users


if __name__ == "__main__":
    create_tables()
    insert_sample_user()
    insert_sample_transaction()
    insert_sample_image()

    users = fetch_users()
    print("\nUsers in database:")
    for user in users:
        print(user)

    print("\n🎉 TASK 2 COMPLETED SUCCESSFULLY 🎉")