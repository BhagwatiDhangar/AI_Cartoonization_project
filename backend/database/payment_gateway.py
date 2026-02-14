import razorpay
from datetime import datetime

# ---------------- RAZORPAY CLIENT ----------------
KEY_ID = "rzp_test_YourKeyID"
KEY_SECRET = "YourKeySecret"

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))

# ---------------- CREATE PAYMENT ORDER ----------------
def create_payment_order(amount_in_inr, receipt_id=None):
    """
    Creates a Razorpay order for payment.
    amount_in_inr: Amount in INR
    receipt_id: Optional unique ID for this order
    """
    if receipt_id is None:
        receipt_id = f"receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    order_data = {
        "amount": int(amount_in_inr*100),  # Amount in paise
        "currency": "INR",
        "receipt": receipt_id,
        "payment_capture": 1  # Auto capture
    }
    try:
        order = client.order.create(data=order_data)
        return order
    except Exception as e:
        raise Exception(f"Error creating Razorpay order: {e}")

# ---------------- VERIFY PAYMENT ----------------
def verify_payment_signature(payment_id, order_id, signature):
    """
    Verify payment signature to ensure payment authenticity.
    """
    try:
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        client.utility.verify_payment_signature(params_dict)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False

# ---------------- UPDATE TRANSACTION STATUS ----------------
def update_transaction_status(transactions_dict, order_id, payment_id, status):
    """
    Store or update transaction details.
    transactions_dict: Dictionary to simulate DB
    """
    transactions_dict[order_id] = {
        "payment_id": payment_id,
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return transactions_dict