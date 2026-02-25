import sqlite3
import os
from datetime import datetime

# =====================================================
# DATABASE CONFIG
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cartoon_app.db")


def create_connection():
    return sqlite3.connect(DB_PATH)


# =====================================================
# CREATE TABLES (CLEAN VERSION)
# =====================================================

def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    # ---------------- USERS TABLE ----------------
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

    # ---------------- IMAGE HISTORY TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ImageHistory (
        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_name TEXT,
        style_applied TEXT,
        download_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
    )
    """)

    # ---------------- TRANSACTIONS TABLE ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        payment_status TEXT,
        transaction_date TEXT,
        payment_method TEXT,
        FOREIGN KEY(user_id) REFERENCES Users(user_id)
    )
    """)

    conn.commit()
    conn.close()

    print("✅ All Tables Created Successfully")


# =====================================================
# STORE IMAGE HISTORY (FIXED)
# =====================================================

def store_image_history(user_id, image_name, style_applied, download_path=None):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ImageHistory 
        (user_id, image_name, style_applied, download_path)
        VALUES (?, ?, ?, ?)
    """, (user_id, image_name, style_applied, download_path))

    conn.commit()
    conn.close()

    print("✅ Image History Saved")


# =====================================================
# FETCH USERS (DEBUG)
# =====================================================

def fetch_users():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()

    conn.close()
    return users


# =====================================================
# SAMPLE TEST DATA (OPTIONAL)
# =====================================================

def insert_sample_user():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO Users
        (username, email, password, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        "testuser",
        "test@gmail.com",
        "123456",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =====================================================
# MAIN (RUN THIS FILE TO CREATE TABLES)
# =====================================================

if __name__ == "__main__":
    create_tables()
    insert_sample_user()
    print("🎉 DATABASE READY 🎉")