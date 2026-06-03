"""Product CRUD routes."""
from flask import Blueprint, request, jsonify
from models.product import Product, CATEGORIES
from routes.middleware import require_auth, require_role
from datetime import datetime

products_bp = Blueprint("products", __name__)


@products_bp.route("/", methods=["GET"])
@require_auth
def get_products():
    query = request.args.get("q", "")
    category = request.args.get("category", "")
    preferences = request.args.getlist("preferences")
    low_stock_only = request.args.get("low_stock") == "true"

    if low_stock_only:
        products = Product.get_low_stock()
    else:
        products = Product.search(query=query, category=category)

    if preferences:
        products = [p for p in products if p.category in preferences]

    return jsonify({
        "products": [p.to_dict() for p in products],
        "total": len(products)
    })


@products_bp.route("/<product_id>", methods=["GET"])
@require_auth
def get_product(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"product": product.to_dict()})


@products_bp.route("/", methods=["POST"])
@require_role("manager")
def create_product():
    data = request.get_json()
    required = ["name", "category", "price", "quantity"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    if data["category"] not in CATEGORIES:
        return jsonify({"error": f"Invalid category. Choose from: {', '.join(CATEGORIES)}"}), 400

    try:
        product = Product.create(
            name=data["name"].strip(),
            category=data["category"],
            price=float(data["price"]),
            quantity=int(data["quantity"]),
            description=data.get("description", ""),
            image=data.get("image", ""),
            low_stock_threshold=int(data.get("low_stock_threshold", 10)),
        )
        return jsonify({"message": "Product created", "product": product.to_dict()}), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@products_bp.route("/<product_id>", methods=["PUT"])
@require_role("manager")
def update_product(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if "name" in data:
        product.name = data["name"].strip()
    if "category" in data:
        if data["category"] not in CATEGORIES:
            return jsonify({"error": "Invalid category"}), 400
        product.category = data["category"]
    if "price" in data:
        product.price = round(float(data["price"]), 2)
    if "quantity" in data:
        product.quantity = int(data["quantity"])
    if "description" in data:
        product.description = data["description"]
    if "image" in data:
        product.image = data["image"]
    if "low_stock_threshold" in data:
        product.low_stock_threshold = int(data["low_stock_threshold"])

    product.save()
    return jsonify({"message": "Product updated", "product": product.to_dict()})


@products_bp.route("/<product_id>", methods=["DELETE"])
@require_role("manager")
def delete_product(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    product.delete()
    return jsonify({"message": "Product deleted"})


@products_bp.route("/categories/list", methods=["GET"])
@require_auth
def get_categories():
    products = Product.get_all()
    category_counts = {}
    for cat in CATEGORIES:
        count = sum(1 for p in products if p.category == cat)
        category_counts[cat] = count
    return jsonify({"categories": CATEGORIES, "counts": category_counts})


@products_bp.route("/stats/overview", methods=["GET"])
@require_auth
def get_stats():
    products = Product.get_all()
    low_stock = [p for p in products if p.is_low_stock]
    out_of_stock = [p for p in products if p.is_out_of_stock]
    total_value = sum(p.price * p.quantity for p in products)
    return jsonify({
        "total_products": len(products),
        "low_stock_count": len(low_stock),
        "out_of_stock_count": len(out_of_stock),
        "total_inventory_value": round(total_value, 2),
        "categories_count": len(set(p.category for p in products)),
    })
