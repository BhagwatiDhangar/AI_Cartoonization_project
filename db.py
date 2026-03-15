
import sqlite3
import os
from datetime import datetime

# ================= DATABASE PATH =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cartoon_app.db")

# ================= CONNECTION =================

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# ================= CREATE TABLES =================

def create_tables():

    conn = create_connection()
    cursor = conn.cursor()

    # ================= USERS TABLE =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT,
        failed_attempts INTEGER DEFAULT 0,
        account_locked INTEGER DEFAULT 0,
        created_at TEXT,
        last_login TEXT
    )
    """)

    # ================= IMAGE HISTORY =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS image_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        image_path TEXT,
        effect TEXT,
        created_at TEXT,
        payment_status TEXT
    )
    """)

    # ================= TRANSACTIONS =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        order_id TEXT,
        payment_id TEXT,
        amount INTEGER,
        status TEXT,
        created_at TEXT
    )
    """)

    # ================= DOWNLOAD HISTORY =================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS downloads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        image_path TEXT,
        download_time TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✅ All Tables Created Successfully")

# ================= STORE IMAGE HISTORY =================

def store_image_history(username, image_path, effect):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO image_history(username,image_path,effect,created_at)
    VALUES(?,?,?,?)
    """,(username,image_path,effect,datetime.now()))

    conn.commit()
    conn.close()

# ================= SAMPLE USER =================

def insert_sample_user():

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO Users(username,email,password,created_at)
    VALUES(?,?,?,?)
    """,(
        "testuser",
        "test@gmail.com",
        "123456",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

# ================= RUN FILE =================

if __name__ == "__main__":

    create_tables()
    insert_sample_user()

    print("🎉 Database Ready")