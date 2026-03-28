# 🍔 Food Delivery System (FastAPI + Streamlit)

A full-stack food delivery application built using **FastAPI (backend)** and **Streamlit (frontend)** with JWT authentication, admin dashboard, and real-time order management.

---

## 🚀 Features

### 👤 User Features
- User Registration & Login (JWT आधारित authentication)
- Browse food items
- Add items to cart
- Place orders
- Track order status
- View order history

### 🛠 Admin Features
- Add food items (with image upload)
- Manage all orders
- Update order status (placed → delivered)
- Role-based access control

---

## 🧠 Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** MongoDB
- **Authentication:** JWT (JSON Web Tokens)
- **File Handling:** UploadFile (images)

---

## 📁 Project Structure
project/
│
├── main.py
├── frontend.py
├── .env
├── .gitignore
├── README.md
│
├── app/
│ ├── routes/
│ │ ├── auth.py
│ │ ├── food.py
│ │ ├── cart.py
│ │ └── order.py
│ │
│ ├── models/
│ │ ├── user.py
│ │ └── order.py
│ │
│ ├── utils/
│ │ └── auth.py
│ │
│ └── database.py
│
└── uploads/