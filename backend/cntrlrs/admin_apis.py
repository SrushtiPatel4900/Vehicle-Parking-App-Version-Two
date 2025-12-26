# backend/cntrlrs/admin_apis.py
from flask import request
from flask_restful import Resource
from sqlalchemy import and_

from datab import db
from model import User, Role, ParkingLot, ParkingSpot, Reservation
from user_datastr import user_datastore

from cache import cache

def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


'''class AdminDashboardAPI(Resource):
    """
    GET /admin
    Returns admin summary: counts of lots, spots, active reservations, users
    """
    def get(self):
        lots = ParkingLot.query.count()
        spots = ParkingSpot.query.count()
        occupied = ParkingSpot.query.filter_by(status=ParkingSpot.STATUS_OCCUPIED).count()
        users = User.query.count()
        active_reservations = Reservation.query.filter(Reservation.leaving_timestamp.is_(None)).count()

        data = {
            "lots": lots,
            "spots": spots,
            "occupied_spots": occupied,
            "users": users,
            "active_reservations": active_reservations
        }
        return success(data, "Admin dashboard summary")'''
class AdminDashboardAPI(Resource):
    @cache.cached(timeout=60) 
    def get(self):
        lots = ParkingLot.query.count()
        spots = ParkingSpot.query.count()

        # FIXED LINE
        occupied = Reservation.query.filter(Reservation.leaving_timestamp.is_(None)).count()

        users = User.query.count()
        active_reservations = occupied  # same thing

        data = {
            "lots": lots,
            "spots": spots,
            "occupied_spots": occupied,
            "users": users,
            "active_reservations": active_reservations
        }
        return success(data, "Admin dashboard summary")


class AdminCreateRoleAPI(Resource):
    """
    Optional: Create roles (not usually needed since create_or_find_role used on init)
    POST /admin/role { name, description }
    """
    def post(self):
        payload = request.get_json() or {}
        name = payload.get("name")
        desc = payload.get("description")
        if not name:
            return error("role name required", 400)
        role = user_datastore.find_or_create_role(name=name, description=desc)
        db.session.commit()
        return success({"id": role.id, "name": role.name}, "Role created/found")
class AdminAllBookingsAPI(Resource):
    """
    GET /admin/bookings
    Return all reservations (for admin view)
    """
    def get(self):
        bookings = Reservation.query.order_by(Reservation.id.desc()).all()
        booking_list = []
        for b in bookings:
            # use existing Reservation.to_dict() but convert datetimes to iso strings if needed
            d = b.to_dict()
            # add user details (safe - admin needs to see who booked)
            if b.user:
                d["user"] = {
                    "id": b.user.id,
                    "username": getattr(b.user, "username", None),
                    "email": getattr(b.user, "email", None)
                }
            else:
                d["user"] = None

            # add spot/lot info if not present in to_dict (optional)
            if not d.get("lot_name") and b.spot and b.spot.lot:
                d["lot_name"] = b.spot.lot.prime_location_name
            if not d.get("spot_number") and b.spot:
                d["spot_number"] = b.spot.spot_number

            booking_list.append(d)

        return success({"bookings": booking_list}, "All bookings")
