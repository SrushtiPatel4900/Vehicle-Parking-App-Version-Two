# backend/tasks/export_csv_task.py
import csv
import os
from datetime import datetime
from celery_app import celery
from app import create_app
from model import User, Reservation
from celery_app import celery

flask_app = create_app()

EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

@celery.task()
def export_user_csv(user_id):
    with flask_app.app_context():
        user = User.query.get(user_id)
        if not user:
            return {"status": "error", "message": "User not found"}

        reservations = Reservation.query.filter_by(user_id=user.id).all()
        filename = f"user_{user.id}_parking_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
        filepath = os.path.join(EXPORT_DIR, filename)

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "reservation_id", "spot_id", "lot_id",
                "parking_timestamp", "leaving_timestamp",
                "parking_cost", "vehicle_number", "remarks"
            ])
            for r in reservations:
                writer.writerow([
                    r.id,
                    r.spot_id,
                    r.spot.lot_id if r.spot else "",
                    r.parking_timestamp.isoformat() if r.parking_timestamp else "",
                    r.leaving_timestamp.isoformat() if r.leaving_timestamp else "",
                    r.parking_cost,
                    r.vehicle_number,
                    r.remarks or ""
                ])

        return {"status": "success", "file_path": filepath, "file_name": filename}
