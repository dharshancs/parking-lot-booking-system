# 🚗 Parking Lot Booking System (Flask)

A full-stack web application for managing parking lots and real-time slot bookings.
Built with Flask using a modular architecture, role-based access control, and a relational database.

This project was developed as part of the **IIT Madras BS – Data Science** program and is intended to demonstrate backend design, CRUD-heavy workflows, and system-level thinking.

---

## 📌 Project Overview

The Parking Lot Booking System allows **users** to search, book, and release parking spots, while **admins** manage parking lots, monitor occupancy, and analyze booking activity.

The application maintains strict consistency between parking lots, individual spots, and booking records, ensuring accurate availability and billing throughout the booking lifecycle.

---

## ✨ Key Features

### 👤 User Features

* User registration and authentication
* Browse parking lots and view real-time availability
* Book parking spots with vehicle details
* Release parking spots with automatic price calculation
* View booking history and spending summary
* Update personal profile details

### 🛠 Admin Features

* Role-based admin authentication
* Create, edit, and delete parking lots
* Dynamically manage parking spots
* Prevent deletion of occupied lots or spots
* Search across users, vehicles, lots, and spots
* View platform-wide usage statistics
* Access recent booking activity
* Admin profile management

---

## 🧱 System Architecture

The application follows a **modular Flask architecture** designed for clarity and scalability:

* **App Factory Pattern** for clean application initialization
* **Blueprint-based routing** for separation of concerns
* **MVC-style structure**

```
controllers/  → Routing and business logic
models/       → Database schema and initialization
templates/    → Jinja2-based HTML views
static/       → CSS and frontend assets
```

This structure mirrors real-world Flask applications used in production environments.

---

## 🛠 Tech Stack

| Layer    | Technologies                 |
| -------- | ---------------------------- |
| Backend  | Python, Flask                |
| Frontend | HTML, CSS, Bootstrap, Jinja2 |
| Database | SQLite                       |
| Auth     | Werkzeug password hashing    |
| Patterns | App Factory, Blueprints      |

---

## 🗃 Database Design

The system uses a relational SQLite database with enforced foreign keys.

### Core Tables

* **USERS** — user accounts and role management
* **PARKING_LOT** — parking lot metadata and capacity
* **PARKING_SPOT** — individual parking slots per lot
* **BOOKING_DETAILS** — booking lifecycle, timestamps, and pricing

All booking actions atomically update:

* Spot availability
* Lot capacity
* Booking status

This ensures data consistency across the system.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd parking-lot-booking
```

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\\Scripts\\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python main.py
```

The application will be available at:

```
http://127.0.0.1:5000
```

---

## 🔐 Demo Credentials

> **Admin Account (for demonstration purposes)**

```
Email: admin@admin.com
Password: admin
```

⚠️ These credentials are auto-initialized for demo and evaluation only.

---

## 📊 What This Project Demonstrates

* Backend system design using Flask
* Role-based access control
* CRUD-heavy workflows with data integrity
* Relational database modeling
* Booking lifecycle management
* Admin dashboards and analytics
* Clean separation of logic and presentation

---

## 📈 Possible Enhancements

* REST API layer for frontend decoupling
* PostgreSQL / MySQL migration
* Pagination for large datasets
* Automated testing (pytest)
* Dockerization
* Payment gateway integration

---

## 👨‍💻 Author

**Dharshan C S**
IIT Madras – BS Data Science
Aspiring Software Engineer

---

## 📄 License

This project is intended for educational and portfolio purposes
