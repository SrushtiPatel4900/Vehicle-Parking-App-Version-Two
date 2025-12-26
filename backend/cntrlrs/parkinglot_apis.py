# backend/cntrlrs/parkinglot_apis.py
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from datab import db
from model import ParkingLot, ParkingSpot

from cache import cache
from cntrlrs.chart_apis import ChartDataAPI
def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class ParkingLotAPI(Resource):
    """
    GET /lots
    POST /lots
    PUT /lots/<int:lot_id>
    DELETE /lots/<int:lot_id>
    """
    @cache.cached(timeout=300)
    def get(self, lot_id=None):
        if lot_id:
            lot = ParkingLot.query.get(lot_id)
            if not lot:
                return error("Parking lot not found", 404)
            return success(lot.to_dict(include_spots=True), "Lot found")
        else:
            lots = ParkingLot.query.all()
            data = [l.to_dict() for l in lots]
            return success({"lots": data}, "List of lots")

    def post(self):
        payload = request.get_json() or {}
        name = payload.get("prime_location_name")
        address = payload.get("address")
        pin_code = payload.get("pin_code")
        price_per_hour = payload.get("price_per_hour", 0.0)
        number_of_spots = int(payload.get("number_of_spots", 0))

        if not name or not address or not pin_code:
            return error("prime_location_name, address and pin_code required", 400)

        lot = ParkingLot(
            prime_location_name=name,
            address=address,
            pin_code=pin_code,
            price_per_hour=price_per_hour,
            number_of_spots=number_of_spots
        )
        db.session.add(lot)
        db.session.commit()

        # Create spots automatically
        lot.create_spots(commit=True)

        cache.delete_memoized(ParkingLotAPI.get)
        cache.delete_memoized(ChartDataAPI.get)
        return success(lot.to_dict(include_spots=True), "Parking lot created")

    def put(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return error("Parking lot not found", 404)

        payload = request.get_json() or {}
        # allow partial updates
        if "prime_location_name" in payload:
            lot.prime_location_name = payload["prime_location_name"]
        if "address" in payload:
            lot.address = payload["address"]
        if "pin_code" in payload:
            lot.pin_code = payload["pin_code"]
        if "price_per_hour" in payload:
            lot.price_per_hour = float(payload["price_per_hour"])
        if "number_of_spots" in payload:
            new_count = int(payload["number_of_spots"])
            if new_count < 0:
                return error("number_of_spots must be >= 0", 400)
            # If decreasing, only allow if the spots that will be removed are available
            current_count = lot.number_of_spots
            if new_count < current_count:
                # find spots to delete
                to_delete_count = current_count - new_count
                # delete from the end: highest numbered spots which are available only
                spots = ParkingSpot.query.filter_by(lot_id=lot.id).order_by(ParkingSpot.id.desc()).all()
                deletable = [s for s in spots if s.is_available()]
                if len(deletable) < to_delete_count:
                    return error("Cannot reduce spots: some spots are occupied", 400)
                for s in deletable[:to_delete_count]:
                    db.session.delete(s)
            lot.number_of_spots = new_count
            if new_count > current_count:
                # create additional spots
                db.session.add(lot)
                db.session.commit()
                lot.create_spots(commit=True)

        db.session.add(lot)
        db.session.commit()

        cache.delete_memoized(ParkingLotAPI.get)
        cache.delete_memoized(ChartDataAPI.get)
        return success(lot.to_dict(include_spots=True), "Parking lot updated")

    def delete(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return error("Parking lot not found", 404)
        # check all spots are available
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status=ParkingSpot.STATUS_OCCUPIED).count()
        if occupied > 0:
            return error("Cannot delete lot: some spots are occupied", 400)
        db.session.delete(lot)
        db.session.commit()

        cache.delete_memoized(ParkingLotAPI.get)
        cache.delete_memoized(ChartDataAPI.get)
        return success({}, "Parking lot deleted")
# Add inside admin_apis.py OR parkinglot_apis.py

# backend/cntrlrs/parkinglot_apis.py

class ParkingLotSpotsAPI(Resource):
    """
    GET /lots/<lot_id>/spots
    Returns all spots of a given parking lot
    """
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return error("Parking lot not found", 404)

        spots = ParkingSpot.query.filter_by(lot_id=lot_id).order_by(ParkingSpot.spot_number).all()

        data = [
            {
                "id": s.id,
                "spot_number": s.spot_number,
                "status": s.status
            }
            for s in spots
        ]

        return {
            "status": "success",
            "spots": data
        }, 200
