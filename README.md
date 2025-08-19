🌀 SmartFlow-SaaS
----------------------------
SmartFlow is a SaaS-based appointment and business management system built with Django and Celery.
It provides core features for managing users, businesses, appointments, notifications, and reporting with support for asynchronous processing.

✨ Features
----------------------------
👤 User Accounts & Authentication

    User registration & login with JWT Authentication
    OTP code verification (via Celery-powered tasks)
    Role-based system (Admin, Business Owner, Customer)

🏢 Business Management

    Create and manage multiple Businesses per user
    Add and manage Services (name, description, price, duration, capacity)
    Services linked directly to Appointments

📅 Appointment System

    Customers can book appointments for business services
    Appointments include date, time, and status (pending, confirmed, canceled)
    Relationships: User ↔ Service ↔ Business

🔔 Notifications

    Celery used for asynchronous notifications (background tasks)
    Notification logs saved in DB (pending, sent, failed)

📑 Reports

    Asynchronous report generation (via Celery worker)
    Supported report types: Appointments & Businesses
    Export available in PDF and Excel (.xlsx)
    Reports saved in DB with downloadable file link
    Automatic notification sent to user when report is ready

⚙️ Architecture & Infrastructure

    Modular Django app structure
    Redis as Celery message broker/result backend
    PostgreSQL as primary database
    Docker Compose setup includes:
        Django Web service
        Celery Worker
        Redis
        PostgreSQL
