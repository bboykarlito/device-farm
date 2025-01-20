import functools

from flask import Blueprint, request
from flaskr.db import get_db

bp = Blueprint("devices", __name__, url_prefix="/api/devices")


@bp.route("/create", methods=("POST",))
def create():
    title = request.json.get("title", "")
    db = get_db()
    db.devices.insert_one({"title": title})

    return {"device": {"title": title}}, 201
