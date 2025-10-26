import re

def validate_email(email: str):
    if not email:
        return False, "Email required"
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        return False, "Invalid email"
    return True, ""

def validate_username(username: str):
    if not username:
        return False, "Username required"
    if not re.match(r"^[A-Za-z0-9_]{3,30}$", username):
        return False, "Username must be 3-30 chars of letters, numbers, underscore"
    return True, ""

def validate_password(password: str):
    if not password:
        return False, "Password required"
    if len(password) < 8 or len(password) > 128:
        return False, "Password length 8-128"
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain a letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain a digit"
    return True, ""
