"""Auth middleware - token validation helper."""
from functools import wraps
from flask import request, jsonify
from models.user import User

ROLE_HIERARCHY = {"user": 0, "cashier": 1, "manager": 2, "admin": 3}


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"error": "No token provided"}), 401
        user = User.get_by_token(token)
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.current_user = user
        return f(*args, **kwargs)
    return decorated


def require_role(min_role):
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated(*args, **kwargs):
            user_role = request.current_user.role
            if ROLE_HIERARCHY.get(user_role, -1) < ROLE_HIERARCHY.get(min_role, 0):
                return jsonify({"error": f"Access denied. Requires '{min_role}' or higher role."}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
