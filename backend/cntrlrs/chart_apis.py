# backend/cntrlrs/chart_apis.py
from flask_restful import Resource
from sqlalchemy import func
from flask import request
from datab import db
from model import ParkingLot, ParkingSpot, Reservation

from cache import cache
def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class ChartDataAPI(Resource):
    """
    GET /charts
    Returns basic metrics useful for charts:
      - spots_by_lot: [{lot_id, lot_name, total_spots, available, occupied}]
      - monthly_reservations_count: [{month, count}] (simple aggregate)
    """
    @cache.cached(timeout=60)
    def get(self):
        lots = ParkingLot.query.all()
        spots_by_lot = []
        for l in lots:
            total = len(l.spots)
            available = sum(1 for s in l.spots if s.status == ParkingSpot.STATUS_AVAILABLE)
            occupied = total - available
            spots_by_lot.append({
                "lot_id": l.id,
                "lot_name": l.prime_location_name,
                "total_spots": total,
                "available": available,
                "occupied": occupied
            })

        # simple monthly reservations (month-year text)
        monthly = db.session.query(func.strftime("%Y-%m", Reservation.parking_timestamp).label("ym"),
                                   func.count(Reservation.id)).group_by("ym").all()
        monthly_reservations = [{"month": m, "count": c} for m, c in monthly]

        data = {"spots_by_lot": spots_by_lot, "monthly_reservations": monthly_reservations}
        return success(data, "Chart data")
    
# backend/cntrlrs/chart_apis.py
from flask_restful import Resource
from flask import request
from sqlalchemy import func
from datab import db
from model import ParkingLot, ParkingSpot, Reservation

def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class UserChartDataAPI(Resource):
    """
    GET /chart/user-dashboard?user_id=5
    Returns user-specific chart data.
    """
    @cache.cached(
    timeout=60,
    key_prefix=lambda: f"user_chart_{request.args.get('user_id')}")
    def get(self):
        # 1) Read user_id from query params
        user_id = request.args.get("user_id")

        if not user_id:
            return error("user_id required", 400)

        try:
            user_id = int(user_id)
        except:
            return error("user_id must be integer", 400)

        lots = ParkingLot.query.all()
        spots_by_lot = []

        for lot in lots:
            total = len(lot.spots)

            # Count spots booked by given user for each lot
            user_booked = (
                db.session.query(Reservation)
                .join(ParkingSpot)
                .filter(
                    Reservation.user_id == user_id,
                    ParkingSpot.lot_id == lot.id
                )
                .count()
            )

            spots_by_lot.append({
                "lot_id": lot.id,
                "lot_name": lot.prime_location_name,
                "total_spots": total,
                "user_booked": user_booked
            })

        return success({"spots_by_lot": spots_by_lot}, "User chart data")
    

