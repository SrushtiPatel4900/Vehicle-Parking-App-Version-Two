# backend/cntrlrs/authentication_apis.py
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from datab import db
from user_datastr import user_datastore
from model import User

# IMPORTANT: using simple Werkzeug hashing
from werkzeug.security import generate_password_hash, check_password_hash


def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200


def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class RegisterAPI(Resource):
    """
    POST /register
    body: { username, email, password }
    """
    def post(self):
        payload = request.get_json() or {}
        username = payload.get("username") or payload.get("name")
        email = payload.get("email")
        password = payload.get("password")

        if not username or not email or not password:
            return error("username, email and password required", 400)

        try:
            # HASH PASSWORD BEFORE SAVING
            user = user_datastore.create_user(
                username=username,
                email=email,
                password=generate_password_hash(password)    # IMPORTANT
            )
            db.session.commit()

            return success(
                {"id": user.id, "email": user.email},
                "User registered"
            )

        except IntegrityError:
            db.session.rollback()
            return error("User with this email already exists", 409)
        except Exception as e:
            db.session.rollback()
            return error(f"Could not register user: {str(e)}", 500)


class CheckEmailAPI(Resource):
    """
    GET /check-email?email=...
    """
    def get(self):
        email = request.args.get("email")
        if not email:
            return error("email query param required", 400)

        user = user_datastore.find_user(email=email)
        if user:
            return success({"exists": True}, "Email exists")

        return success({"exists": False}, "Email available")


class LoginAPI(Resource):
    """
    POST /login
    body: { email, password }
    """
    def post(self):
        payload = request.get_json() or {}
        email = payload.get("email")
        password = payload.get("password")
        
        if not email or not password:
            return error("email and password required", 400)

        user = user_datastore.find_user(email=email)
        if not user:
            return error("Invalid credentials", 401)

        # CHECK HASHED PASSWORD
        if not check_password_hash(user.password, password):
            return error("Invalid credentials", 401)

        return success(
            {"id": user.id, "email": user.email, "username": user.username, "role": user.roles[0].name if user.roles else "user"},
            "Login success"
        )


class LogoutAPI(Resource):
    """
    POST /logout (placeholder)
    """
    def post(self):
        return success({}, "Logged out")
    
