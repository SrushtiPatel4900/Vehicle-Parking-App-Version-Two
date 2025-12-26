# backend/app.py

from flask import Flask
from flask_security import Security
from flask_restful import Api
from flask_cors import CORS

# --- Core Imports (Corrected Paths) ---
from datab import db
from config import Config
from user_datastr import user_datastore

# --- API Controllers ---
from cntrlrs.authentication_apis import (
    LoginAPI, LogoutAPI, RegisterAPI, CheckEmailAPI
)


from cntrlrs.admin_apis import AdminDashboardAPI, AdminAllBookingsAPI
from cntrlrs.parkinglot_apis import ParkingLotAPI, ParkingLotSpotsAPI
from cntrlrs.parkingspot_apis import ParkingSpotAPI, AdminSpotDetailsAPI
from cntrlrs.booking_apis import (
    ReserveSpotAPI,
    ReleaseSpotAPI,
    UserBookingsAPI
)
from cntrlrs.user_apis import UserListAPI
from cntrlrs.chart_apis import ChartDataAPI, UserChartDataAPI
from cntrlrs.export_csv_apis import ExportCSVAPI, DownloadCSVAPI
from werkzeug.security import generate_password_hash

from cache import cache
# ---------------------------------------------------
# Application Factory
# ---------------------------------------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Redis Cache Setup
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_HOST"] = "localhost"
    app.config["CACHE_REDIS_PORT"] = 6379
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes

    cache.init_app(app)
    
    # Initialize DB + Security
    db.init_app(app)
    security = Security(app, user_datastore)

    # API prefix
    api = Api(app, prefix="/api")

    # Create DB + Auto-create admin
    with app.app_context():
        db.create_all()

        # Create roles
        admin_role = user_datastore.find_or_create_role(
            name='admin', description='Administrator'
        )
        user_role = user_datastore.find_or_create_role(
            name='user', description='Regular User'
        )

        # Create default admin
        if not user_datastore.find_user(email="admin@gmail.com"):
            user_datastore.create_user(
                email="admin@gmail.com",
                username="admin",
                password=generate_password_hash("admin123"),
                roles=[admin_role]
            )

        db.session.commit()

    return app


# ---------------------------------------------------
# Init App
# ---------------------------------------------------
app = create_app()
api = Api(app, prefix="/api")

# CORS for Vue frontend
CORS(app, origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173"
])


# ---------------------------------------------------
# Register API Endpoints
# ---------------------------------------------------

# Authentication
api.add_resource(LoginAPI,        "/auth/login")
api.add_resource(LogoutAPI,       "/auth/logout")
api.add_resource(RegisterAPI,     "/auth/register")
api.add_resource(CheckEmailAPI,   "/auth/check-email")

# Admin
api.add_resource(AdminDashboardAPI, "/admin")
api.add_resource(AdminSpotDetailsAPI, "/admin/spot-details/<int:spot_id>")

# Parking Lots
api.add_resource(ParkingLotAPI,
                 "/lots",
                 "/lots/<int:lot_id>")

# Parking Spots
api.add_resource(ParkingSpotAPI,
                 "/spots",
                 "/spots/<int:spot_id>")
from cntrlrs.lot_spots_apis import SpotsByLotAPI
api.add_resource(SpotsByLotAPI, "/lots/<int:lot_id>/spots")


# Bookings
api.add_resource(ReserveSpotAPI,     "/reserve")
api.add_resource(ReleaseSpotAPI,     "/bookings/release/<int:booking_id>")
api.add_resource(UserBookingsAPI,    "/bookings/user")

# Users
api.add_resource(UserListAPI, "/users")

# Charts
api.add_resource(ChartDataAPI, "/chart/admin")
api.add_resource(UserChartDataAPI, "/chart/user-dashboard")
# CSV Export
api.add_resource(ExportCSVAPI, "/export-csv")
api.add_resource(DownloadCSVAPI, "/download-csv")

# ... (other imports)

# then register
api.add_resource(AdminAllBookingsAPI, "/admin/bookings")
api.add_resource(ParkingLotSpotsAPI, "/admin/lots/<int:lot_id>/spots")

# ---------------------------------------------------
# Root Route (Health Check)
# ---------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return {
        "message": "🚗 Vehicle Parking App - V2 Backend Running!",
        "status": "ok",
        "api_prefix": "/api"
    }, 200


# ---------------------------------------------------
# Main Entry
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
