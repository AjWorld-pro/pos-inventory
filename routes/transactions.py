"""Transaction/POS routes."""
from flask import Blueprint, request, jsonify
from models.transaction import Transaction
from models.product import Product
from routes.middleware import require_auth, require_role
from datetime import datetime, timedelta

transactions_bp = Blueprint("transactions", __name__)


@transactions_bp.route("/", methods=["GET"])
@require_auth
def get_transactions():
    start = request.args.get("start")
    end = request.args.get("end")
    if start and end:
        txns = Transaction.get_by_date_range(start, end)
    else:
        txns = Transaction.get_all()
    txns_sorted = sorted(txns, key=lambda t: t.created_at, reverse=True)
    return jsonify({
        "transactions": [t.to_dict() for t in txns_sorted],
        "total": len(txns_sorted)
    })


@transactions_bp.route("/<txn_id>", methods=["GET"])
@require_auth
def get_transaction(txn_id):
    txn = Transaction.get_by_id(txn_id)
    if not txn:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"transaction": txn.to_dict()})


@transactions_bp.route("/", methods=["POST"])
@require_role("user")
def create_transaction():
    data = request.get_json()
    items = data.get("items", [])
    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    payment_method = data.get("payment_method", "cash")
    amount_paid = float(data.get("amount_paid", 0))
    discount = float(data.get("discount", 0))

    # Validate and deduct stock
    validated_items = []
    for item in items:
        product = Product.get_by_id(item["product_id"])
        if not product:
            return jsonify({"error": f"Product {item['product_id']} not found"}), 404
        qty = int(item["quantity"])
        if product.quantity < qty:
            return jsonify({"error": f"Insufficient stock for '{product.name}'. Available: {product.quantity}"}), 400
        validated_items.append({
            "product_id": product.id,
            "product_name": product.name,
            "category": product.category,
            "price": product.price,
            "quantity": qty,
            "subtotal": round(product.price * qty, 2),
        })

    subtotal = round(sum(i["subtotal"] for i in validated_items), 2)
    tax_rate = float(data.get("tax_rate", 0))
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal - discount + tax, 2)

    if payment_method == "cash" and amount_paid < total:
        return jsonify({"error": f"Amount paid (${amount_paid}) is less than total (${total})"}), 400

    # Deduct stock
    for item in validated_items:
        product = Product.get_by_id(item["product_id"])
        product.quantity -= item["quantity"]
        product.save()

    user = request.current_user
    txn = Transaction.create(
        items=validated_items,
        total=total,
        cashier_id=user.id,
        cashier_name=user.name,
        payment_method=payment_method,
        amount_paid=amount_paid,
        discount=discount,
        tax=tax,
    )
    return jsonify({"message": "Sale completed", "transaction": txn.to_dict()}), 201


@transactions_bp.route("/reports/daily", methods=["GET"])
@require_role("manager")
def daily_report():
    date = request.args.get("date", datetime.utcnow().date().isoformat())
    txns = [t for t in Transaction.get_all() if t.created_at.startswith(date)]
    items_sold = {}
    for t in txns:
        for item in t.items:
            key = item["product_name"]
            items_sold[key] = items_sold.get(key, 0) + item["quantity"]

    return jsonify({
        "date": date,
        "total_transactions": len(txns),
        "total_revenue": round(sum(t.total for t in txns), 2),
        "items_sold": [{"name": k, "quantity": v} for k, v in
                       sorted(items_sold.items(), key=lambda x: x[1], reverse=True)],
    })


@transactions_bp.route("/reports/weekly", methods=["GET"])
@require_role("manager")
def weekly_summary():
    return jsonify({"summary": Transaction.get_summary(days=7)})


@transactions_bp.route("/reports/monthly", methods=["GET"])
@require_role("manager")
def monthly_summary():
    return jsonify({"summary": Transaction.get_summary(days=30)})


@transactions_bp.route("/reports/overview", methods=["GET"])
@require_auth
def overview():
    today = datetime.utcnow().date().isoformat()
    yesterday = (datetime.utcnow().date() - timedelta(days=1)).isoformat()
    week_start = (datetime.utcnow().date() - timedelta(days=6)).isoformat()
    month_start = (datetime.utcnow().date() - timedelta(days=29)).isoformat()

    all_txns = Transaction.get_all()
    today_txns = [t for t in all_txns if t.created_at.startswith(today)]
    yesterday_txns = [t for t in all_txns if t.created_at.startswith(yesterday)]
    week_txns = [t for t in all_txns if t.created_at[:10] >= week_start]
    month_txns = [t for t in all_txns if t.created_at[:10] >= month_start]

    def revenue(txns):
        return round(sum(t.total for t in txns), 2)

    return jsonify({
        "today": {"transactions": len(today_txns), "revenue": revenue(today_txns)},
        "yesterday": {"transactions": len(yesterday_txns), "revenue": revenue(yesterday_txns)},
        "week": {"transactions": len(week_txns), "revenue": revenue(week_txns)},
        "month": {"transactions": len(month_txns), "revenue": revenue(month_txns)},
        "total": {"transactions": len(all_txns), "revenue": revenue(all_txns)},
    })
