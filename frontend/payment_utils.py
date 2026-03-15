import uuid
import datetime

# ---------------- CREATE ORDER ----------------
def create_payment_order(user_id, amount=10):

    order_id = "order_" + str(uuid.uuid4())

    return {
        "order_id": order_id,
        "amount": amount,
        "status": "pending"
    }


# ---------------- UPDATE TRANSACTION ----------------
def update_transaction_status(cursor, conn,
                              user_id,
                              order_id,
                              amount,
                              status):

    cursor.execute("""
        INSERT INTO transactions
        (user_id, order_id, amount, status, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        order_id,
        amount,
        status,
        datetime.datetime.now()
    ))

    conn.commit()