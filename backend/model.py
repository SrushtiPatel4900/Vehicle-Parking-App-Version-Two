# backend/models.py
import uuid
from datetime import datetime
from sqlalchemy.orm import validates
from datab import db

# -----------------------------
# ROLE / USER MODELS
# -----------------------------
class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # hashed by Flask-Security / auth layer
    active = db.Column(db.Boolean, default=True, nullable=False)

    # Flask-Security unique identifiers
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=True)

    # Audit
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    roles = db.relationship("Role", secondary="user_roles", backref=db.backref("users", lazy="dynamic"))
    reservations = db.relationship("Reservation", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# -----------------------------
# PARKING LOT
# -----------------------------
class ParkingLot(db.Model):
    __tablename__ = "parking_lots"

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False, default=0.0)
    number_of_spots = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.String(512), nullable=True)

    # Relationship: spots are deleted if the lot is deleted
    spots = db.relationship("ParkingSpot", backref="lot", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ParkingLot {self.prime_location_name} (spots={self.number_of_spots})>"

    def available_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status=ParkingSpot.STATUS_AVAILABLE).count()

    def occupied_spots_count(self):
        return ParkingSpot.query.filter_by(lot_id=self.id, status=ParkingSpot.STATUS_OCCUPIED).count()

    def to_dict(self, include_spots=False):
        data = {
            "id": self.id,
            "prime_location_name": self.prime_location_name,
            "address": self.address,
            "pin_code": self.pin_code,
            "price_per_hour": self.price_per_hour,
            "number_of_spots": self.number_of_spots,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_spots:
            data["spots"] = [s.to_dict() for s in self.spots]
        return data

    def create_spots(self, commit=True, prefix="S"):
        """
        Create parking spots to match self.number_of_spots.
        If spots exist, it will create the missing ones to reach the desired count.
        Spot numbering scheme: {prefix}{1..n} e.g. S1, S2...
        """
        existing_count = len(self.spots)
        to_create = self.number_of_spots - existing_count
        created = []
        for i in range(existing_count + 1, self.number_of_spots + 1):
            spot_number = f"{prefix}{i}"
            spot = ParkingSpot(lot_id=self.id, spot_number=spot_number)
            db.session.add(spot)
            created.append(spot)
        if commit and to_create > 0:
            db.session.commit()
        return created


# -----------------------------
# PARKING SPOT
# -----------------------------
class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"

    STATUS_AVAILABLE = "A"
    STATUS_OCCUPIED = "O"

    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id", ondelete="CASCADE"), nullable=False)
    # Spot number must be unique per lot - enforced logically (combination); simple unique on (lot_id, spot_number)
    spot_number = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(1), default=STATUS_AVAILABLE, nullable=False)  # A=Available, O=Occupied
    vehicle_number = db.Column(db.String(20), nullable=True)
    reserved_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reservations = db.relationship("Reservation", backref="spot", lazy=True, cascade="all, delete-orphan")

    __table_args__ = (
        db.UniqueConstraint("lot_id", "spot_number", name="uix_lot_spotnumber"),
    )

    def __repr__(self):
        return f"<ParkingSpot {self.spot_number} ({self.status})>"

    def is_available(self):
        return self.status == self.STATUS_AVAILABLE

    def occupy(self, vehicle_number: str):
        """
        Mark spot as occupied and set vehicle_number & reserved_at.
        """
        if not self.is_available():
            raise ValueError("Spot is not available to occupy.")
        self.status = self.STATUS_OCCUPIED
        self.vehicle_number = vehicle_number
        self.reserved_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        return self

    def release(self):
        """
        Mark spot as available and clear vehicle info.
        """
        if self.is_available():
            raise ValueError("Spot is already available.")
        self.status = self.STATUS_AVAILABLE
        self.vehicle_number = None
        self.reserved_at = None
        db.session.add(self)
        db.session.commit()
        return self

    def to_dict(self, include_reservations=False):
        data = {
            "id": self.id,
            "lot_id": self.lot_id,
            "spot_number": self.spot_number,
            "status": self.status,
            "vehicle_number": self.vehicle_number,
            "reserved_at": self.reserved_at.isoformat() if self.reserved_at else None,
        }
        if include_reservations:
            data["reservations"] = [r.to_dict() for r in self.reservations]
        return data


# -----------------------------
# RESERVATION (BOOKING)
# -----------------------------
class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spots.id", ondelete="CASCADE"), nullable=False)

    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)

    parking_cost = db.Column(db.Float, nullable=True)
    vehicle_number = db.Column(db.String(20), nullable=False)

    remarks = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Reservation id={self.id} user={self.user_id} spot={self.spot_id}>"

    def calculate_cost(self, price_per_hour: float) -> float:
        """
        Calculate parking cost using parking_timestamp and leaving_timestamp.
        If leaving_timestamp is None, returns 0.0 (not finalized).
        """
        if not self.leaving_timestamp:
            return 0.0
        duration_seconds = (self.leaving_timestamp - self.parking_timestamp).total_seconds()
        duration_hours = duration_seconds / 3600.0
        cost = round(duration_hours * float(price_per_hour), 2)
        return cost

    def finalize(self, leaving_ts: datetime = None, commit=True):
        """
        Finalize reservation: set leaving_timestamp, compute parking_cost using the lot's price.
        Also releases the associated ParkingSpot.
        """
        if self.leaving_timestamp:
            # already finalized
            return self

        self.leaving_timestamp = leaving_ts or datetime.utcnow()

        # derive price_per_hour from linked spot -> lot
        if not self.spot or not self.spot.lot:
            raise RuntimeError("Cannot finalize reservation: spot or lot not found.")

        price_per_hour = self.spot.lot.price_per_hour
        self.parking_cost = self.calculate_cost(price_per_hour)

        # release the spot
        try:
            self.spot.release()
        except Exception:
            # If release raises (e.g., spot already available), continue to save reservation
            pass

        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def to_dict(self):
        lot = self.spot.lot if self.spot else None

        return {
            "id": self.id,
            "user_id": self.user_id,
            "spot_id": self.spot_id,

            # NEW FIELDS needed by frontend
            "lot_name": lot.prime_location_name if lot else None,
            "spot_number": self.spot.spot_number if self.spot else None,
            "status": "active" if not self.leaving_timestamp else "released",
            "cost": self.parking_cost,

            # Existing fields
            "parking_timestamp": self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            "leaving_timestamp": self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            "parking_cost": self.parking_cost,
            "vehicle_number": self.vehicle_number,
            "remarks": self.remarks,
        }



# -----------------------------
# VALIDATIONS / HELPERS
# -----------------------------
@validates("User", "email")
def validate_email(key, email_value):
    # note: SQLAlchemy validates decorator usage typically attaches to model class methods.
    # Provided as placeholder — actual validation should be done in controller/service layer.
    return email_value
