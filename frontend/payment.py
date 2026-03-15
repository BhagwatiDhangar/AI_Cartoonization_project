import sqlite3
import uuid
from datetime import datetime
import os

# ================= DATABASE PATH =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "cartoon_app.db")

# ================= CREATE CONNECTION =================

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# ================= CREATE PAYMENT ORDER =================

def create_payment_order(username, amount):

    order_id = "order_" + str(uuid.uuid4())[:8]

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions
    (username, order_id, amount, status, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        order_id,
        amount,
        "pending",
        datetime.now()
    ))

    conn.commit()
    conn.close()

    return order_id


# ================= VERIFY PAYMENT =================

def verify_payment(order_id):

    payment_id = "pay_" + str(uuid.uuid4())[:8]

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE transactions
    SET payment_id=?, status=?
    WHERE order_id=?
    """, (
        payment_id,
        "success",
        order_id
    ))

    conn.commit()
    conn.close()

    return payment_id


# ================= GET USER PAYMENTS =================

def get_user_transactions(username):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT order_id, payment_id, amount, status, created_at
    FROM transactions
    WHERE username=?
    ORDER BY id DESC
    """, (username,))

    data = cursor.fetchall()

    conn.close()

    return data