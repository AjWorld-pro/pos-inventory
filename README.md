# POSIFY - POS & Inventory Management System

A Point-of-Sale and Inventory Management web application built with Python (Flask) backend and HTML/CSS/JavaScript frontend.

---

## Features

- Auth System - Register/Login with token-based authentication; Admin, Manager, Cashier roles
- Product Feed - Personalized dashboard with category preferences
- Inventory Management - Add, edit, delete products with category, price, quantity, images
- Point of Sale (POS) - Fast checkout with cart management and receipts
- Low Stock Alerts - Real-time notifications when items fall below threshold
- Reports & Analytics - Daily/weekly/monthly revenue, top products, category breakdown
- User Management - Admin can create, view, and update user roles
- Settings - Profile editing, preferences, system toggles
- Fully Responsive - Works on mobile, tablet and desktop

---

## Default Accounts

| Role    | Username | Password   | Access |
|---------|----------|------------|--------|
| Admin   | admin    | admin123   | Full access |

Admin can create new users and assign roles from Settings > User Management.

---

## Tech Stack

### Backend
- Python 3.11+ / Flask - REST API
- OOP models - Product, User, Transaction, CartLinkedList
- Doubly-linked list for cart management
- JSON file storage

### Frontend
- Vanilla HTML/CSS/JavaScript
- Chart.js for charts
- Google Fonts (Playfair Display + DM Sans)

---

## Project Structure

```
pos-inventory/
  app.py                  Flask entry point + seeding
  requirements.txt
  Procfile                Render deployment
  render.yaml
  vercel.json
  models/
    linked_list.py        Cart linked list
    product.py            Product model
    user.py               User model
    transaction.py        Transaction model
    storage.py            File I/O persistence
  routes/
    auth.py               /api/auth/*
    products.py           /api/products/*
    transactions.py       /api/transactions/*
    middleware.py         Token auth decorator
  data/                   JSON data files (auto-created)
  static/
    index.html            Login / Register
    dashboard.html        Dashboard with product feed
    inventory.html        Product management
    pos.html              Point of Sale
    reports.html          Analytics
    settings.html         Profile, preferences, user management
    css/main.css          Global stylesheet
    js/
      api.js              API client
      sidebar.js          Shared navigation
```

---

## Local Setup

### Clone and Install

```
git clone https://github.com/YOUR_USERNAME/posify.git
cd posify
pip install -r requirements.txt
```

### Run

```
python app.py
```

Open http://localhost:5000 and log in with admin / admin123.

---

## Deploy on Render (Recommended)

1. Push to GitHub
2. Go to render.com > New > Web Service
3. Connect your GitHub repo
4. Render auto-detects render.yaml - click Deploy

Important: Add a Disk in Render settings (path: /opt/render/project/src/data, 1GB) for JSON data persistence.

---

## Deploy on Vercel

```
npm install -g vercel
vercel --prod
```

Note: Vercel is serverless - data won't persist between requests. Use Render for full persistence.

---

## Role Permissions

| Feature                    | Cashier | Manager | Admin |
|----------------------------|---------|---------|-------|
| View Dashboard             | Yes     | Yes     | Yes   |
| Use POS / Checkout         | Yes     | Yes     | Yes   |
| View Inventory             | Yes     | Yes     | Yes   |
| Add/Edit/Delete Products   | No      | Yes     | Yes   |
| View Reports               | No      | Yes     | Yes   |
| Manage Users               | No      | No      | Yes   |
| System Settings            | No      | No      | Yes   |

---

## API Endpoints

### Auth
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login
- POST /api/auth/logout - Logout
- GET  /api/auth/me - Get current user
- PUT  /api/auth/preferences - Update preferences
- GET  /api/auth/users - List all users (Admin)
- PUT  /api/auth/users/:id - Update user role (Admin)

### Products
- GET  /api/products/ - List / search products
- POST /api/products/ - Create product
- GET  /api/products/:id - Get one product
- PUT  /api/products/:id - Update product
- DELETE /api/products/:id - Delete product
- GET  /api/products/stats/overview - Inventory stats

### Transactions
- GET  /api/transactions/ - List transactions
- POST /api/transactions/ - Complete a sale
- GET  /api/transactions/reports/daily - Daily report
- GET  /api/transactions/reports/weekly - 7-day summary
- GET  /api/transactions/reports/overview - Revenue overview

---

## License

MIT License
