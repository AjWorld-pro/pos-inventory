# 🏪 POSIFY — POS & Inventory Management System

A modern, full-stack Point-of-Sale and Inventory Management web application built with **Python (Flask)** backend and **HTML/CSS/JavaScript** frontend. Features a personalized Quora-style product feed, OOP architecture, linked list cart, and File I/O data persistence.

---

## ✨ Features

- 🔐 **Auth System** — Register/Login with JWT-style tokens; Admin, Manager, Cashier roles
- ✨ **Personalized Feed** — Quora-inspired popup on first login to choose product category preferences
- 📦 **Inventory Management** — Add, edit, delete products with category, price, quantity, images
- 🛒 **Point of Sale (POS)** — Fast checkout, cart with linked list, receipts, payment methods
- ⚠️ **Low Stock Alerts** — Real-time notifications when items fall below threshold
- 📊 **Reports & Analytics** — Daily/weekly/monthly revenue charts, top products, category breakdown
- 👥 **User Management** — Admin can create, view, and update roles for all users
- ⚙️ **Settings** — Profile editing, preferences, system toggles
- 📱 **Fully Responsive** — Works on mobile, tablet and desktop

---

## 🎨 Design

- **Colors:** Emerald Green `#059669` · White · Gold `#D97706`
- **Fonts:** Playfair Display (headings) + DM Sans (body)
- **Theme:** Modern, professional, Quora-inspired personalization

---

## 🔑 Default Accounts

| Role    | Email                  | Password   | Access |
|---------|------------------------|------------|--------|
| Admin   | admin@posify.com       | admin123   | Full access — users, settings, reports, inventory, POS |
| Manager | (register via admin)   | your choice| Inventory, POS, Reports |
| Cashier | (register via admin)   | your choice| Dashboard, POS only |

**Admin** can create new users and assign roles from **Settings → User Management**.

---

## 🏗 Tech Stack

### Backend
- **Python 3.11+** + **Flask** — REST API
- **OOP** — `Product`, `User`, `Transaction`, `CartLinkedList` classes
- **Linked List** — Doubly-linked list for cart management
- **File I/O** — JSON file storage in `/data/` directory

### Frontend
- **Vanilla HTML/CSS/JavaScript** — No framework required
- **Chart.js** — Revenue and category charts
- **Google Fonts** — Playfair Display + DM Sans

---

## 📁 Project Structure

```
pos-inventory/
├── app.py                  # Flask entry point + seeding
├── requirements.txt
├── Procfile                # Render deployment
├── render.yaml             # Render config
├── vercel.json             # Vercel config
├── models/
│   ├── linked_list.py      # Cart doubly-linked list (OOP)
│   ├── product.py          # Product OOP model
│   ├── user.py             # User OOP model
│   ├── transaction.py      # Transaction OOP model
│   └── storage.py          # File I/O persistence layer
├── routes/
│   ├── auth.py             # /api/auth/* — login, register, users
│   ├── products.py         # /api/products/* — CRUD + stats
│   ├── transactions.py     # /api/transactions/* — POS + reports
│   └── middleware.py       # Token auth decorator
├── data/                   # JSON data files (auto-created)
└── static/
    ├── index.html          # Login / Register
    ├── dashboard.html      # Home feed + preferences
    ├── inventory.html      # Product catalog management
    ├── pos.html            # Point of Sale terminal
    ├── reports.html        # Analytics & reports
    ├── settings.html       # Profile, preferences, user mgmt
    ├── css/main.css        # Global stylesheet
    └── js/
        ├── api.js          # API client + utilities
        └── sidebar.js      # Shared navigation
```

---

## 🚀 Local Setup

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/posify.git
cd posify
pip install -r requirements.txt
```

### 2. Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) and log in with `admin@posify.com` / `admin123`.

---

## 🌐 Deploy on Render (Recommended — Free)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**
5. Done! Your app is live at `https://posify-app.onrender.com`

**Important:** Add a **Disk** in Render settings (path: `/opt/render/project/src/data`, 1GB) so JSON data persists between deploys.

---

## ☁️ Deploy on Vercel

```bash
npm install -g vercel
vercel --prod
```

> Note: Vercel is serverless — data won't persist between requests. Use Render for full persistence.

---

## 🔒 Role Permissions

| Feature              | Cashier | Manager | Admin |
|----------------------|---------|---------|-------|
| View Dashboard       | ✅      | ✅      | ✅    |
| Use POS / Checkout   | ✅      | ✅      | ✅    |
| View Inventory       | ✅      | ✅      | ✅    |
| Add/Edit/Delete Products | ❌  | ✅      | ✅    |
| View Reports         | ❌      | ✅      | ✅    |
| Manage Users         | ❌      | ❌      | ✅    |
| System Settings      | ❌      | ❌      | ✅    |

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET  | `/api/auth/me` | Get current user |
| PUT  | `/api/auth/preferences` | Update preferences |
| GET  | `/api/auth/users` | List all users (Admin) |
| PUT  | `/api/auth/users/:id` | Update user role (Admin) |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List / search products |
| POST | `/api/products/` | Create product |
| GET | `/api/products/:id` | Get one product |
| PUT | `/api/products/:id` | Update product |
| DELETE | `/api/products/:id` | Delete product |
| GET | `/api/products/stats/overview` | Inventory stats |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transactions/` | List transactions |
| POST | `/api/transactions/` | Complete a sale |
| GET | `/api/transactions/reports/daily` | Daily report |
| GET | `/api/transactions/reports/weekly` | 7-day summary |
| GET | `/api/transactions/reports/overview` | Revenue overview |

---

## 🧠 OOP & Data Structures

- **`CartLinkedList`** — Doubly linked list; each cart item is a `CartNode` with `prev/next` pointers
- **`Product`** — Encapsulates product data + CRUD class methods
- **`User`** — Handles auth, tokens, preferences; password hashing with SHA-256
- **`Transaction`** — Immutable sale records with auto receipt numbers
- **`Storage`** — Generic File I/O JSON CRUD layer used by all models

---

## 📄 License

MIT License — free to use and modify.
