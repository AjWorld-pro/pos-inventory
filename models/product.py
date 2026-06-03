"""Product model using OOP."""
import uuid
from datetime import datetime
from models.storage import Storage

product_storage = Storage("products.json")

CATEGORIES = [
    "Electronics", "Clothing & Apparel", "Food & Beverages",
    "Health & Beauty", "Home & Garden", "Sports & Outdoors",
    "Toys & Games", "Office Supplies", "Automotive", "Books & Media"
]


class Product:
    """Represents a product in the inventory system."""

    LOW_STOCK_DEFAULT = 10

    def __init__(self, name: str, category: str, price: float, quantity: int,
                 description: str = "", image: str = "", low_stock_threshold: int = None,
                 product_id: str = None, created_at: str = None, updated_at: str = None):
        self.id = product_id or str(uuid.uuid4())
        self.name = name
        self.category = category
        self.price = round(float(price), 2)
        self.quantity = int(quantity)
        self.description = description
        self.image = image or "https://placehold.co/600x400/10B981/ffffff?text=POSIFY"
        self.low_stock_threshold = low_stock_threshold or self.LOW_STOCK_DEFAULT
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or datetime.utcnow().isoformat()

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        return self.quantity == 0

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description,
            "image": self.image,
            "low_stock_threshold": self.low_stock_threshold,
            "is_low_stock": self.is_low_stock,
            "is_out_of_stock": self.is_out_of_stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data["name"],
            category=data["category"],
            price=data["price"],
            quantity=data["quantity"],
            description=data.get("description", ""),
            image=data.get("image", ""),
            low_stock_threshold=data.get("low_stock_threshold"),
            product_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    # --- CRUD class methods ---

    @classmethod
    def get_all(cls):
        return [cls.from_dict(d) for d in product_storage.get_all()]

    @classmethod
    def get_by_id(cls, product_id: str):
        data = product_storage.get_by_id(product_id)
        return cls.from_dict(data) if data else None

    @classmethod
    def create(cls, **kwargs):
        product = cls(**kwargs)
        product_storage.create(product.to_dict())
        return product

    def save(self):
        self.updated_at = datetime.utcnow().isoformat()
        data = self.to_dict()
        if product_storage.get_by_id(self.id):
            product_storage.update(self.id, data)
        else:
            product_storage.create(data)
        return self

    def delete(self):
        return product_storage.delete(self.id)

    @classmethod
    def search(cls, query: str = "", category: str = ""):
        products = cls.get_all()
        if query:
            q = query.lower()
            products = [p for p in products if q in p.name.lower() or q in p.description.lower()]
        if category:
            products = [p for p in products if p.category == category]
        return products

    @classmethod
    def get_low_stock(cls):
        return [p for p in cls.get_all() if p.is_low_stock]

    def restock(self, amount: int):
        self.quantity += amount
        self.save()
