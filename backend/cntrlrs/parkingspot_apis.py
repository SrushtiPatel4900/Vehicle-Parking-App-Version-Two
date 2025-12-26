# backend/cntrlrs/parkingspot_apis.py
from flask_restful import Resource

from datab import db
from model import ParkingSpot, User, Reservation

def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class ParkingSpotAPI(Resource):
    '''
    GET /spots -> list
    GET /spots/<id> -> details
    
    def get(self, spot_id=None):
        if spot_id:
            spot = ParkingSpot.query.get(spot_id)
            if not spot:
                return error("Spot not found", 404)
            return success(spot.to_dict(include_reservations=True), "Spot found")
        else:
            spots = ParkingSpot.query.all()
            data = [s.to_dict() for s in spots]
            return success({"spots": data}, "List of spots")'''
    def get(self, spot_id=None):
        if not spot_id:
            return error("Spot ID required", 400)

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return error("Spot not found", 404)

        data = {
            "spot_id": spot.id,
            "spot_number": spot.spot_number,
            "status": spot.status,
            "lot_name": spot.lot.prime_location_name if spot.lot else None,
        }

        # If spot is occupied → return parked vehicle info
        if spot.status == "O":
            active = (
                Reservation.query
                .filter_by(spot_id=spot.id, leaving_timestamp=None)
                .first()
            )

            if active:
                user = User.query.get(active.user_id)
                data.update({
                    "vehicle_number": active.vehicle_number,
                    "reserved_at": active.parking_timestamp.isoformat(),
                    "user_name": user.username if user else None,
                    "user_email": user.email if user else None
                })
        else:
            data.update({
                "vehicle_number": None,
                "reserved_at": None,
                "user_name": None,
                "user_email": None
            })

        return success(data, "Spot details loaded")

class AdminSpotDetailsAPI(Resource):
    def get(self, spot_id):
        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return error("Spot not found", 404)

        active = Reservation.query.filter_by(
            spot_id=spot.id, leaving_timestamp=None
        ).first()

        if active:
            user = User.query.get(active.user_id)
            data = {
                "user": {
                    "name": user.username,
                    "email": user.email
                },
                "vehicle_number": active.vehicle_number,
                "start_time": active.parking_timestamp.isoformat(),
            }
        else:
            data = {
                "user": {"name": None, "email": None},
                "vehicle_number": None,
                "start_time": None,
                "cost_till_now": 0,
            }

        return success(data, "Spot details loaded")
