from flask import Blueprint, request
import os
from .. import db


bp = Blueprint('redis', __name__, url_prefix='/redis')


@bp.route("/room/", methods=["POST"])
def create_room():
    data = request.get_json()

    if db.setnx("room_pk", 1) == 1:
        room_code = 1
    else:
        room_code = int(db.get("room_pk")) + 1
        db.set("room_pk", room_code)
    total = data["total"]
    current = data["current"]
    avail = data["avail"]

    event = {"room_code": room_code,
             "total": total,
             "current": current,
             "avail": avail}

    db.set(f"room {room_code}", event)

    if avail:
        return {"id": room_code, "message": f"Room {room_code} {current}/{total} is available."}
    else:
        return {"id": room_code, "message": f"Room {room_code} {current}/{total} is not available."}




