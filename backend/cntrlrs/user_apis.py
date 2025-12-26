# backend/cntrlrs/user_apis.py
from flask_restful import Resource

from datab import db
from model import User

def success(data=None, message="OK"):
    return {"status": "success", "data": data or {}, "message": message}, 200

def error(message="Error", code=400):
    return {"status": "error", "data": {}, "message": message}, code


class UserListAPI(Resource):
    """
    GET /users -> list users
    """
    def get(self):
        users = User.query.all()
        data = [u.to_dict() for u in users]
        return success({"users": data}, "List of users")
