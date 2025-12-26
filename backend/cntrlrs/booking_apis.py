# backend/cntrlrs/booking_apis.py
from flask import request
from flask_restful import Resource
from datetime import datetime

from datab import db
from model import ParkingLot, ParkingSpot, Reservation, User
from cntrlrs.chart_apis import ChartDataAPI
from cntrlrs.parkinglot_apis import ParkingLotAPI
from cntrlrs.lot_spots_apis import SpotsByLotAPI
from cache import cache

def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class ReserveSpotAPI(Resource):
    """
    POST /reserve
    body: { user_id, lot_id, vehicle_number }
    Allocates first available spot in the specified lot.
    """
    def post(self):
        payload = request.get_json() or {}
        user_id = payload.get("user_id")
        lot_id = payload.get("lot_id")
        vehicle_number = payload.get("vehicle_number")

        if not user_id or not lot_id or not vehicle_number:
            return error("user_id, lot_id and vehicle_number required", 400)

        user = User.query.get(user_id)
        if not user:
            return error("User not found", 404)

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return error("Parking lot not found", 404)

        # first available spot (by id ascending)
        spot = ParkingSpot.query.filter_by(lot_id=lot.id, status=ParkingSpot.STATUS_AVAILABLE).order_by(ParkingSpot.id.asc()).first()
        if not spot:
            return error("No available spots in this lot", 400)

        # create reservation and occupy spot
        reservation = Reservation(user_id=user.id, spot_id=spot.id, vehicle_number=vehicle_number, parking_timestamp=datetime.utcnow())
        db.session.add(reservation)
        db.session.flush()  # get reservation.id

        # occupy spot
        spot.occupy(vehicle_number)

        db.session.add(reservation)
        db.session.commit()
        # IMPORTANT: cache invalidation
        cache.delete_memoized(SpotsByLotAPI.get, lot_id)
        cache.delete_memoized(ChartDataAPI.get)
        cache.delete_memoized(ParkingLotAPI.get)

        return success({"reservation_id": reservation.id, "spot_id": spot.id}, "Spot reserved")


class ReleaseSpotAPI(Resource):
    """
    POST /release/<int:booking_id>
    Finalize reservation and compute cost.
    """
    def post(self, booking_id):
        reservation = Reservation.query.get(booking_id)
        if not reservation:
            return error("Reservation not found", 404)
        if reservation.leaving_timestamp:
            return error("Reservation already released", 400)

        reservation.finalize()

        spot = ParkingSpot.query.get(reservation.spot_id)
        lot_id = spot.lot_id
        # IMPORTANT: cache invalidation
        cache.delete_memoized(SpotsByLotAPI.get, lot_id)
        cache.delete_memoized(ChartDataAPI.get)
        cache.delete_memoized(ParkingLotAPI.get)

        return success(reservation.to_dict(), "Reservation finalized and spot released")


class UserBookingsAPI(Resource):
    """
    GET /bookings/user
    frontend passes user_id as query param: ?user_id=5
    """
    def get(self):
        user_id = request.args.get("user_id")
        if not user_id:
            return error("user_id is required", 400)

        user = User.query.get(user_id)
        if not user:
            return error("User not found", 404)

        bookings = [r.to_dict() for r in user.reservations]
        return success({"bookings": bookings}, "User bookings")

    

