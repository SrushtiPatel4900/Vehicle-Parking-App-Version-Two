from flask_security import SQLAlchemyUserDatastore
from model import User, Role

from datab import db


user_datastore = SQLAlchemyUserDatastore(db, User, Role)