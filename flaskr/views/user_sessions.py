from flask import Blueprint, request
from flaskr.db import get_db
from flask_jwt_extended import create_access_token
from bcrypt import checkpw, gensalt, hashpw
from pydantic import ValidationError
from flaskr.models.user import User
from flaskr.utils.handle_pydantic_errors import handle_pydentic_errors

bp = Blueprint("user_sessions", __name__, url_prefix="/api/users")


@bp.route("/", methods=("POST",))
def register():
    db = get_db()

    try:
        user = User(**request.json)
    except ValidationError as e:
        return {"errors": handle_pydentic_errors(e.errors())}, 400

    if db.users.find_one({"username": user.username}) is not None:
        return {"errors": {"username": "has alredy been taken"}}, 400

    db.users.insert_one(
        {
            "username": user.username,
            "password": __hash_password(user.password),
        }
    )

    access_token = create_access_token(identity=user.username)
    return {"user": {"username": user.username}, "access_token": access_token}, 201


@bp.route("/login", methods=("POST",))
def login():
    db = get_db()

    try:
        user_data = User(**request.json)
    except ValidationError as e:
        return {"errors": handle_pydentic_errors(e.errors())}, 400

    user = db.users.find_one({"username": user_data.username})
    if user is None or not checkpw(user_data.password.encode("utf-8"), user.get("password")):
        return {"error": "Invalid username or password"}, 401

    access_token = create_access_token(identity=user_data.username)
    return {"user": {"username": user_data.username}, "access_token": access_token}, 200


def __hash_password(password):
    bytes = password.encode("utf-8")
    salt = gensalt()
    return hashpw(bytes, salt)
