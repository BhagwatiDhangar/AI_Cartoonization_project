import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    if not re.search(r"[A-Z]", password):
        return False, "Must contain uppercase letter"

    if not re.search(r"[a-z]", password):
        return False, "Must contain lowercase letter"

    if not re.search(r"[0-9]", password):
        return False, "Must contain a number"

    if not re.search(r"[!@#$%^&*]", password):
        return False, "Must contain special character"

    return True, "Valid"