"""User model using OOP."""
import uuid
import hashlib
import secrets
from datetime import datetime
from models.storage import Storage

user_storage = Storage("users.json")


class User:
    """Represents a user in the POS system."""

    VALID_ROLES = ["user", "cashier", "manager", "admin"]

    def __init__(self, name: str, username: str, email: str, password_hash: str = "",
                 role: str = "user", preferences: list = None,
                 user_id: str = None, token: str = None,
                 preferences_set: bool = False,
                 created_at: str = None):
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.username = username.lower()
        self.email = email.lower()
        self.password_hash = password_hash
        self.role = role
        self.preferences = preferences or []
        self.token = token
        self.preferences_set = preferences_set
        self.created_at = created_at or datetime.utcnow().isoformat()

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password_hash == self.hash_password(password)

    def generate_token(self) -> str:
        self.token = secrets.token_hex(32)
        return self.token

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "preferences": self.preferences,
            "token": self.token,
            "preferences_set": self.preferences_set,
            "created_at": self.created_at,
        }

    def to_public_dict(self):
        """Return user data without sensitive info."""
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "preferences": self.preferences,
            "preferences_set": self.preferences_set,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            username=data.get("username", data["name"].lower().replace(" ", "_")),
            email=data["email"],
            password_hash=data.get("password_hash", ""),
            role=data.get("role", "user"),
            preferences=data.get("preferences", []),
            user_id=data.get("id"),
            token=data.get("token"),
            preferences_set=data.get("preferences_set", False),
            created_at=data.get("created_at"),
        )

    @classmethod
    def get_all(cls):
        return [cls.from_dict(d) for d in user_storage.get_all()]

    @classmethod
    def get_by_id(cls, user_id: str):
        data = user_storage.get_by_id(user_id)
        return cls.from_dict(data) if data else None

    @classmethod
    def get_by_email(cls, email: str):
        data = user_storage.get_by_field("email", email.lower())
        return cls.from_dict(data) if data else None

    @classmethod
    def get_by_username(cls, username: str):
        data = user_storage.get_by_field("username", username.lower())
        return cls.from_dict(data) if data else None

    @classmethod
    def get_by_token(cls, token: str):
        data = user_storage.get_by_field("token", token)
        return cls.from_dict(data) if data else None

    @classmethod
    def register(cls, name: str, username: str, email: str, password: str, role: str = "user"):
        if cls.get_by_username(username):
            return None, "Username already taken"
        if cls.get_by_email(email):
            return None, "Email already registered"
        user = cls(
            name=name,
            username=username,
            email=email,
            password_hash=cls.hash_password(password),
            role=role,
        )
        user.generate_token()
        user_storage.create(user.to_dict())
        return user, None

    @classmethod
    def login(cls, username: str, password: str):
        user = cls.get_by_username(username)
        if not user or not user.check_password(password):
            return None, "Invalid username or password"
        user.generate_token()
        user_storage.update(user.id, {"token": user.token})
        return user, None

    def logout(self):
        self.token = None
        user_storage.update(self.id, {"token": None})

    def update_preferences(self, preferences: list):
        self.preferences = preferences
        self.preferences_set = True
        user_storage.update(self.id, {"preferences": preferences, "preferences_set": True})

    def save(self):
        data = self.to_dict()
        if user_storage.get_by_id(self.id):
            user_storage.update(self.id, data)
        else:
            user_storage.create(data)
        return self
