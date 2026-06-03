"""
POS & Inventory Management System
Flask Backend Entry Point
"""
import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__, static_folder="static", static_url_path="")
    CORS(app, origins="*")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "pos-inventory-secret-key-2024")

    # Register blueprints
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(products_bp, url_prefix="/api/products")
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions")

    # Seed initial data if empty
    seed_data()

    # Serve static frontend
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path.startswith("api/"):
            return jsonify({"error": "Not found"}), 404
        static_folder = app.static_folder
        if path and os.path.exists(os.path.join(static_folder, path)):
            return send_from_directory(static_folder, path)
        return send_from_directory(static_folder, "index.html")

    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, "index.html")

    return app


def seed_data():
    """Seed sample products and admin user if data is empty."""
    from models.product import Product, CATEGORIES
    from models.user import User

    # Seed admin user
    if not User.get_by_username("admin"):
        User.register("Admin User", "admin", "admin@posify.com", "admin123", "admin")
        print("[OK] Admin user seeded: admin / admin123")

    # Seed products
    existing = Product.get_all()
    if existing:
        first = existing[0]
        if first.image == Product.DEFAULT_IMAGE:
            for p in existing:
                p.delete()
            existing = []
    if not existing:
        sample_products = [
            {"name": "MacBook Pro 14\"", "category": "Electronics", "price": 1999.99, "quantity": 15, "description": "Apple M3 Pro chip, 18GB RAM", "low_stock_threshold": 5, "image": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&h=400&fit=crop"},
            {"name": "iPhone 15 Pro", "category": "Electronics", "price": 1199.99, "quantity": 30, "description": "Titanium design, 48MP camera", "low_stock_threshold": 8, "image": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=600&h=400&fit=crop"},
            {"name": "Samsung 4K Monitor", "category": "Electronics", "price": 449.99, "quantity": 12, "description": "27-inch UHD IPS display", "low_stock_threshold": 3, "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&h=400&fit=crop"},
            {"name": "Wireless Earbuds", "category": "Electronics", "price": 129.99, "quantity": 50, "description": "Active noise cancellation", "low_stock_threshold": 10, "image": "https://images.pexels.com/photos/11677122/pexels-photo-11677122.jpeg?w=600&h=400&fit=crop"},
            {"name": "USB-C Hub", "category": "Electronics", "price": 49.99, "quantity": 4, "description": "7-in-1 multiport adapter", "low_stock_threshold": 5, "image": "https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=600&h=400&fit=crop"},
            {"name": "Men's Polo Shirt", "category": "Clothing & Apparel", "price": 34.99, "quantity": 80, "description": "Premium cotton blend", "low_stock_threshold": 15, "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=600&h=400&fit=crop"},
            {"name": "Women's Sneakers", "category": "Clothing & Apparel", "price": 89.99, "quantity": 45, "description": "Comfortable everyday sneakers", "low_stock_threshold": 10, "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=400&fit=crop"},
            {"name": "Denim Jacket", "category": "Clothing & Apparel", "price": 74.99, "quantity": 8, "description": "Classic fit, stonewashed", "low_stock_threshold": 10, "image": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600&h=400&fit=crop"},
            {"name": "Sports Running Cap", "category": "Clothing & Apparel", "price": 19.99, "quantity": 60, "description": "Moisture-wicking fabric", "low_stock_threshold": 15, "image": "https://images.unsplash.com/photo-1556306535-0f09f53773c0?w=600&h=400&fit=crop"},
            {"name": "Organic Green Tea", "category": "Food & Beverages", "price": 12.99, "quantity": 120, "description": "Premium Japanese matcha blend", "low_stock_threshold": 20, "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=600&h=400&fit=crop"},
            {"name": "Cold Brew Coffee 500ml", "category": "Food & Beverages", "price": 6.99, "quantity": 85, "description": "Single origin Ethiopian beans", "low_stock_threshold": 20, "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&h=400&fit=crop"},
            {"name": "Protein Bar Pack x12", "category": "Food & Beverages", "price": 24.99, "quantity": 40, "description": "Chocolate fudge, 20g protein", "low_stock_threshold": 10, "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&h=400&fit=crop"},
            {"name": "Vitamin C 1000mg", "category": "Health & Beauty", "price": 15.99, "quantity": 7, "description": "60 tablets with zinc", "low_stock_threshold": 10, "image": "https://images.unsplash.com/photo-1550572017-edd951b55104?w=600&h=400&fit=crop"},
            {"name": "Face Moisturizer SPF50", "category": "Health & Beauty", "price": 29.99, "quantity": 35, "description": "Lightweight daily moisturizer", "low_stock_threshold": 10, "image": "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=400&fit=crop"},
            {"name": "Yoga Mat Premium", "category": "Sports & Outdoors", "price": 54.99, "quantity": 22, "description": "Non-slip 6mm thickness", "low_stock_threshold": 5, "image": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=600&h=400&fit=crop"},
            {"name": "Resistance Bands Set", "category": "Sports & Outdoors", "price": 22.99, "quantity": 55, "description": "5 resistance levels", "low_stock_threshold": 10, "image": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=600&h=400&fit=crop"},
            {"name": "LEGO Architecture Set", "category": "Toys & Games", "price": 69.99, "quantity": 18, "description": "789 pieces, age 12+", "low_stock_threshold": 5, "image": "https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=600&h=400&fit=crop"},
            {"name": "Desk Organizer Bamboo", "category": "Office Supplies", "price": 27.99, "quantity": 33, "description": "Eco-friendly bamboo organizer", "low_stock_threshold": 8, "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=600&h=400&fit=crop"},
            {"name": "Mechanical Keyboard", "category": "Office Supplies", "price": 119.99, "quantity": 14, "description": "TKL layout, Cherry MX switches", "low_stock_threshold": 5, "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&h=400&fit=crop"},
            {"name": "Scented Candle Set", "category": "Home & Garden", "price": 38.99, "quantity": 3, "description": "Set of 3, 40hr burn time", "low_stock_threshold": 8, "image": "https://images.unsplash.com/photo-1602523961358-f9f03f3a9f08?w=600&h=400&fit=crop"},
        ]
        for p in sample_products:
            Product.create(**p)
        print(f"[OK] {len(sample_products)} sample products seeded")


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("POS inventory running on http://localhost:" + str(port))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")
