from backend.database.db_config import get_connection
from utils.security import hash_password, verify_password
from backend.validators import validate_email, validate_password
from datetime import datetime


def register_user(username, email, password):

    if not validate_email(email):
        return False, "Invalid email format"

    valid, message = validate_password(password)
    if not valid:
        return False, message

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE username=? OR email=?",
                   (username, email))

    if cursor.fetchone():
        conn.close()
        return False, "Username or Email already exists"

    password_hash = hash_password(password)

    cursor.execute("""
    INSERT INTO Users(username, email, password_hash, created_at)
    VALUES (?, ?, ?, ?)
    """, (username, email, password_hash,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

    return True, "Registration Successful"


def login_user(identifier, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_id, username, email, password_hash, failed_attempts, last_login
    FROM Users
    WHERE username=? OR email=?
    """, (identifier, identifier))

    user = cursor.fetchone()

    if not user:
        conn.close()
        return False, "User does not exist"

    user_id, username, email, stored_hash, failed_attempts, last_login = user

    if failed_attempts >= 5:
        conn.close()
        return False, "Account locked due to 5 failed attempts"

    if not verify_password(password, stored_hash):
        failed_attempts += 1
        cursor.execute("UPDATE Users SET failed_attempts=? WHERE user_id=?",
                       (failed_attempts, user_id))
        conn.commit()
        conn.close()
        return False, f"Invalid password ({failed_attempts}/5 attempts)"

    cursor.execute("""
    UPDATE Users
    SET failed_attempts=0, last_login=?
    WHERE user_id=?
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))

    conn.commit()
    conn.close()

    return True, {
        "user_id": user_id,
        "username": username,
        "email": email,
        "last_login": last_login
    }
def save_history(user_id, style, image_name, processing_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ImageHistory(user_id, style, image_name, processing_time, created_at)
    VALUES (?, ?, ?, ?, datetime('now'))
    """, (user_id, style, image_name, processing_time))

    conn.commit()
    conn.close()