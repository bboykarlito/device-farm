from flask import Blueprint, request
from flaskr.db import get_db
from flask_jwt_extended import create_access_token
from bcrypt import checkpw, gensalt, hashpw

bp = Blueprint("user_sessions", __name__, url_prefix="/api/users")


@bp.route("/", methods=("POST",))
def register():
    db = get_db()
    username = request.json.get("username")
    password = request.json.get("password")

    error = None
    if not username:
        error = "Username is required."

    if not password:
        error = "Password is required."

    if db.users.find_one({"username": username}) is not None:
        error = "Username has alredy been taken"

    if error:
        return {"error": error}, 400

    db.users.insert_one(
        {
            "username": username,
            "password": __hash_password(password),
        }
    )

    access_token = create_access_token(identity=username)
    return {"user": {"username": username}, "access_token": access_token}, 201


@bp.route("/login", methods=("POST",))
def login():
    db = get_db()
    username = request.json.get("username")
    password = request.json.get("password")

    error = None
    if not username:
        error = "Username is required."

    if not password:
        error = "Password is required."

    if error:
        return {"error": error}, 400

    user = db.users.find_one({"username": username})
    if user is None or not checkpw(password.encode("utf-8"), user.get("password")):
        return {"error": "Invalid username or password"}, 401

    access_token = create_access_token(identity=username)
    return {"user": {"username": username}, "access_token": access_token}, 200


def __hash_password(password):
    bytes = password.encode("utf-8")
    salt = gensalt()
    return hashpw(bytes, salt)
