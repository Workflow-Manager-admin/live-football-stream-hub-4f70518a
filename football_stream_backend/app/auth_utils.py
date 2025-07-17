"""
Authentication utility code for registration, login, and token validation.
(For demonstration purposes only: uses in-memory storage. DO NOT use for production.)
"""
import uuid
import hashlib
import secrets
import time

from .models import USERS

SECRET_KEY = "change_this_for_real_deployments"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, password):
    return stored_password == hash_password(password)

# PUBLIC_INTERFACE
def register_user(username, password):
    """Register a new user if username isn't taken."""
    if username in USERS:
        return False, "Username already exists."
    user_id = str(uuid.uuid4())
    USERS[username] = {
        "id": user_id,
        "username": username,
        "password_hash": hash_password(password),
        "created": int(time.time())
    }
    return True, user_id

# PUBLIC_INTERFACE
def authenticate_user(username, password):
    """Check username/password and return a fake token if valid."""
    user = USERS.get(username)
    if not user or not verify_password(user["password_hash"], password):
        return False, None
    # Generate fake JWT-like session token
    token = secrets.token_hex(16)
    user["token"] = token
    user["token_expiry"] = int(time.time()) + 3600  # expires in 1hr
    return True, token

# PUBLIC_INTERFACE
def validate_token(token):
    """Validate a token and return associated user, if token is valid and not expired."""
    for user in USERS.values():
        if user.get("token") == token and int(time.time()) < user.get("token_expiry", 0):
            return user
    return None
