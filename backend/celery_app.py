# backend/celery_app.py
from celery import Celery
from celery.schedules import crontab

from datetime import datetime
import csv, os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from model import User, Reservation
from mail import send_email

# -----------------------------
# INIT FLASK APP
# -----------------------------
flask_app = create_app()

# -----------------------------
# INIT CELERY
# -----------------------------
celery = Celery(
    "vehicle_app",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

celery.autodiscover_tasks(['tasks'])

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
)

# ---------------------------------------------------------------------------------------------------
# 1️⃣ DAILY REMINDER — If user has NOT booked today → send email reminder
# ---------------------------------------------------------------------------------------------------
@celery.task()
def send_daily_reminder():
    with flask_app.app_context():
        today = datetime.now().date()

        users = User.query.all()

        for u in users:
            # Check if user has a booking today
            booked_today = Reservation.query.filter(
                Reservation.user_id == u.id,
                Reservation.parking_timestamp >= datetime(today.year, today.month, today.day)
            ).first()

            if booked_today:
                continue  # Skip users who already booked

            html = f"""
            <div style='font-family:Arial; padding:20px;'>
                <h2>Daily Reminder 🚗</h2>
                <p>Hi <b>{u.username}</b>,</p>
                <p>You have not booked any parking today.</p>
                <p>Please book a parking spot if needed.</p>
                <br>
                <p>— Vehicle Parking App</p>
            </div>
            """

            send_email(u.email, "Daily Parking Reminder", html)

        return "Daily reminders sent."


# ---------------------------------------------------------------------------------------------------
# 2️⃣ USER CSV EXPORT — Async Job
# ---------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------
# 3️⃣ MONTHLY PARKING REPORT — First day of month
# ---------------------------------------------------------------------------------------------------
@celery.task()
def send_monthly_report():
    with flask_app.app_context():
        users = User.query.all()

        for u in users:
            # month filter
            now = datetime.now()
            month_start = datetime(now.year, now.month, 1)

            reservations = Reservation.query.filter(
                Reservation.user_id == u.id,
                Reservation.parking_timestamp >= month_start
            ).all()

            total_bookings = len(reservations)
            total_amount = sum(r.parking_cost or 0 for r in reservations)

            lot_count = {}
            for r in reservations:
                if r.spot and r.spot.lot:
                    name = r.spot.lot.prime_location_name
                    lot_count[name] = lot_count.get(name, 0) + 1

            most_used = max(lot_count, key=lot_count.get) if lot_count else "None"

            html = f"""
            <h2>📅 Monthly Parking Report</h2>
            <p>Hello <b>{u.username}</b>,</p>

            <h3>Summary for {now.strftime("%B %Y")}:</h3>
            <ul>
                <li><b>Total Bookings:</b> {total_bookings}</li>
                <li><b>Most Used Parking Lot:</b> {most_used}</li>
                <li><b>Total Amount Spent:</b> ₹{total_amount}</li>
            </ul>

            <p>Thanks for using the app!</p>
            """

            send_email(u.email, "Your Monthly Parking Report", html)

        return "Monthly reports sent."


# ---------------------------------------------------------------------------------------------------
# CELERY BEAT SCHEDULES
# ---------------------------------------------------------------------------------------------------
celery.conf.beat_schedule = {
    # Every 1 minute for testing
    "daily-reminder-task": {
        "task": "celery_app.send_daily_reminder",
        "schedule": crontab(minute="*/1"),
    },
    "monthly-report-task": {
        "task": "celery_app.send_monthly_report",
        "schedule": crontab(minute="*/2"),
    },
}
