"""Auth routes: register, login, logout, get profile."""
from flask import Blueprint, request, jsonify
from models.user import User
from routes.middleware import require_auth

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = (data.get("name") or "").strip()
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password", "")
    role = data.get("role", "user")

    if not name or not username or not email or not password:
        return jsonify({"error": "Name, username, email, and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    user, error = User.register(name, username, email, password, role)
    if error:
        return jsonify({"error": error}), 409

    return jsonify({
        "message": "Registration successful",
        "token": user.token,
        "user": user.to_public_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = (data.get("username") or "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user, error = User.login(username, password)
    if error:
        return jsonify({"error": error}), 401

    return jsonify({
        "message": "Login successful",
        "token": user.token,
        "user": user.to_public_dict()
    })


@auth_bp.route("/logout", methods=["POST"])
@require_auth
def logout():
    request.current_user.logout()
    return jsonify({"message": "Logged out"})


@auth_bp.route("/me", methods=["GET"])
@require_auth
def me():
    return jsonify({"user": request.current_user.to_public_dict()})


@auth_bp.route("/preferences", methods=["PUT"])
@require_auth
def update_preferences():
    data = request.get_json()
    preferences = data.get("preferences", [])
    if not isinstance(preferences, list):
        return jsonify({"error": "Preferences must be a list"}), 400
    request.current_user.update_preferences(preferences)
    return jsonify({
        "message": "Preferences updated",
        "preferences": preferences
    })


@auth_bp.route("/users", methods=["GET"])
@require_auth
def list_users():
    if request.current_user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403
    users = User.get_all()
    return jsonify({"users": [u.to_public_dict() for u in users]})


@auth_bp.route("/users/<user_id>", methods=["PUT"])
@require_auth
def update_user(user_id):
    if request.current_user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if "role" in data:
        valid_roles = User.VALID_ROLES
        if data["role"] not in valid_roles:
            return jsonify({"error": f"Role must be one of: {', '.join(valid_roles)}"}), 400
        user.role = data["role"]
        from models.user import user_storage
        user_storage.update(user.id, {"role": user.role})
    return jsonify({"message": "User updated", "user": user.to_public_dict()})


@auth_bp.route("/users/<user_id>", methods=["DELETE"])
@require_auth
def delete_user(user_id):
    if request.current_user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403
    if user_id == request.current_user.id:
        return jsonify({"error": "Cannot delete your own account"}), 400
    from models.user import user_storage
    deleted = user_storage.delete(user_id)
    if not deleted:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"})


@auth_bp.route("/profile", methods=["PUT"])
@require_auth
def update_profile():
    data = request.get_json()
    user = request.current_user
    if "name" in data:
        user.name = data["name"].strip()
    from models.storage import Storage
    from models.user import user_storage
    user_storage.update(user.id, {"name": user.name})
    return jsonify({"message": "Profile updated", "user": user.to_public_dict()})
