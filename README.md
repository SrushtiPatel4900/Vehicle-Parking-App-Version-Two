# 🚗 Vehicle Parking Management App – V2

Vehicle Parking Management App – V2 is a scalable multi-user web application designed to efficiently manage parking lots, parking spots, and vehicle reservations. The system supports **role-based access control** with separate **Admin** and **User** workflows.

The backend is built using **Flask** with a modular, RESTful API architecture, while the frontend is developed using **Vue.js** for a responsive, component-based user interface styled with **Bootstrap 5**.

---

## ✨ Features

### 🔐 Admin Module
- Create and manage parking lots
- Automatically generate parking spots
- Monitor real-time parking occupancy
- Manage registered users
- View analytical dashboards using **Chart.js**

### 👤 User Module
- User registration and authentication
- Reserve the first available parking spot
- Release reserved parking spots
- View complete parking history

---

## 🛠️ Tech Stack

**Backend**
- Flask (RESTful APIs)
- SQLAlchemy ORM
- Flask-Login / JWT Authentication

**Frontend**
- Vue.js
- Bootstrap 5

**Database**
- SQLite

**Caching & Background Tasks**
- Redis (API caching)
- Celery (asynchronous & scheduled tasks)

**Analytics**
- Chart.js

---

## ⚙️ Functional Highlights
- Role-based access (Admin / User)
- Secure authentication and session management
- Real-time occupancy tracking
- Asynchronous tasks for:
  - Daily parking reminders
  - Monthly email reports
- Modular backend architecture for scalability

---

## 🚀 Project Objectives
- Demonstrate end-to-end **full-stack development**
- Implement **API-driven architecture**
- Apply **backend automation using Celery**
- Design a system scalable for real-world use cases

---

## 📌 Future Enhancements
- Cloud deployment (AWS / GCP)
- Payment gateway integration
- Mobile-friendly PWA version
- Advanced analytics and reporting
- Multi-city and multi-branch support

---

## 👨‍💻 Author
Developed as part of an academic and practical full-stack development project to demonstrate scalable system design and modern web technologies.
