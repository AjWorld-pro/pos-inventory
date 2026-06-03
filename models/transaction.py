"""Transaction model using OOP."""
import uuid
from datetime import datetime
from models.storage import Storage

transaction_storage = Storage("transactions.json")


class Transaction:
    """Represents a completed POS transaction/sale."""

    def __init__(self, items: list, total: float, cashier_id: str,
                 cashier_name: str, payment_method: str = "cash",
                 amount_paid: float = 0, transaction_id: str = None,
                 receipt_number: str = None, created_at: str = None,
                 discount: float = 0, tax: float = 0):
        self.id = transaction_id or str(uuid.uuid4())
        self.items = items  # list of dicts from cart
        self.subtotal = round(sum(i["subtotal"] for i in items), 2)
        self.discount = round(float(discount), 2)
        self.tax = round(float(tax), 2)
        self.total = round(float(total), 2)
        self.amount_paid = round(float(amount_paid), 2)
        self.change = round(self.amount_paid - self.total, 2)
        self.cashier_id = cashier_id
        self.cashier_name = cashier_name
        self.payment_method = payment_method
        self.receipt_number = receipt_number or self._generate_receipt_number()
        self.created_at = created_at or datetime.utcnow().isoformat()

    @staticmethod
    def _generate_receipt_number() -> str:
        now = datetime.utcnow()
        suffix = str(uuid.uuid4())[:6].upper()
        return f"RCP-{now.strftime('%Y%m%d')}-{suffix}"

    def to_dict(self):
        return {
            "id": self.id,
            "items": self.items,
            "subtotal": self.subtotal,
            "discount": self.discount,
            "tax": self.tax,
            "total": self.total,
            "amount_paid": self.amount_paid,
            "change": self.change,
            "cashier_id": self.cashier_id,
            "cashier_name": self.cashier_name,
            "payment_method": self.payment_method,
            "receipt_number": self.receipt_number,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            items=data["items"],
            total=data["total"],
            cashier_id=data["cashier_id"],
            cashier_name=data.get("cashier_name", ""),
            payment_method=data.get("payment_method", "cash"),
            amount_paid=data.get("amount_paid", 0),
            transaction_id=data.get("id"),
            receipt_number=data.get("receipt_number"),
            created_at=data.get("created_at"),
            discount=data.get("discount", 0),
            tax=data.get("tax", 0),
        )

    @classmethod
    def create(cls, **kwargs):
        txn = cls(**kwargs)
        transaction_storage.create(txn.to_dict())
        return txn

    @classmethod
    def get_all(cls):
        return [cls.from_dict(d) for d in transaction_storage.get_all()]

    @classmethod
    def get_by_id(cls, txn_id: str):
        data = transaction_storage.get_by_id(txn_id)
        return cls.from_dict(data) if data else None

    @classmethod
    def get_today(cls):
        today = datetime.utcnow().date().isoformat()
        all_txns = cls.get_all()
        return [t for t in all_txns if t.created_at.startswith(today)]

    @classmethod
    def get_by_date_range(cls, start_date: str, end_date: str):
        all_txns = cls.get_all()
        return [t for t in all_txns if start_date <= t.created_at[:10] <= end_date]

    @classmethod
    def get_daily_revenue(cls, date: str = None):
        date = date or datetime.utcnow().date().isoformat()
        txns = [t for t in cls.get_all() if t.created_at.startswith(date)]
        return round(sum(t.total for t in txns), 2)

    @classmethod
    def get_summary(cls, days: int = 7):
        from datetime import timedelta
        results = []
        for i in range(days - 1, -1, -1):
            d = (datetime.utcnow().date() - timedelta(days=i)).isoformat()
            txns = [t for t in cls.get_all() if t.created_at.startswith(d)]
            results.append({
                "date": d,
                "transactions": len(txns),
                "revenue": round(sum(t.total for t in txns), 2),
            })
        return results
