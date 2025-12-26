from flask_restful import Resource
from model import ParkingLot, ParkingSpot
from datab import db

from cache import cache

def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class SpotsByLotAPI(Resource):
    """
    GET /lots/<lot_id>/spots
    Returns all spots in a given parking lot
    """
    @cache.cached(timeout=120)
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return error("Parking lot not found", 404)

        spots = ParkingSpot.query.filter_by(lot_id=lot_id)\
                                 .order_by(ParkingSpot.id.asc()).all()

        return success({
            "lot_name": lot.prime_location_name,
            "spots": [s.to_dict() for s in spots]
        }, "Spots loaded")

def clear_spots_cache(lot_id):
    cache.delete_memoized(SpotsByLotAPI.get, lot_id)