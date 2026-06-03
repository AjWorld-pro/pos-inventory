"""
Linked List implementation used for the shopping cart.
Each cart item is stored as a node in the doubly linked list.
"""


class CartNode:
    """Node in the cart linked list."""

    def __init__(self, product_id: str, product_name: str, price: float, quantity: int, image: str = ""):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.image = image
        self.subtotal = round(price * quantity, 2)
        self.prev = None
        self.next = None

    def update_quantity(self, quantity: int):
        self.quantity = quantity
        self.subtotal = round(self.price * quantity, 2)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity": self.quantity,
            "image": self.image,
            "subtotal": self.subtotal,
        }


class CartLinkedList:
    """Doubly linked list representing a shopping cart."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def add_item(self, product_id: str, product_name: str, price: float, quantity: int = 1, image: str = "") -> CartNode:
        """Add item or increment quantity if already exists."""
        existing = self.find_by_product_id(product_id)
        if existing:
            existing.update_quantity(existing.quantity + quantity)
            return existing

        node = CartNode(product_id, product_name, price, quantity, image)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def remove_item(self, product_id: str) -> bool:
        """Remove item from cart by product_id."""
        node = self.find_by_product_id(product_id)
        if not node:
            return False
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        self._size -= 1
        return True

    def update_quantity(self, product_id: str, quantity: int) -> bool:
        node = self.find_by_product_id(product_id)
        if not node:
            return False
        if quantity <= 0:
            return self.remove_item(product_id)
        node.update_quantity(quantity)
        return True

    def find_by_product_id(self, product_id: str):
        current = self.head
        while current:
            if current.product_id == product_id:
                return current
            current = current.next
        return None

    def clear(self):
        self.head = self.tail = None
        self._size = 0

    def get_total(self) -> float:
        total = 0.0
        current = self.head
        while current:
            total += current.subtotal
            current = current.next
        return round(total, 2)

    def to_list(self) -> list:
        items = []
        current = self.head
        while current:
            items.append(current.to_dict())
            current = current.next
        return items

    @property
    def size(self):
        return self._size

    def __len__(self):
        return self._size
