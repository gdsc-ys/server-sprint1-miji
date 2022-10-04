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

    db.setnx(f"room:{room_code}:room_code", room_code)
    db.setnx(f"room:{room_code}:total", total)
    db.setnx(f"room:{room_code}:current", current)
    db.setnx(f"room:{room_code}:avail", avail)

    db.sadd("rooms", room_code)
    if avail:
        return {"id": room_code, "message": f"Room {room_code} {current}/{total} is available."}
    else:
        return {"id": room_code, "message": f"Room {room_code} {current}/{total} is not available."}


@bp.route("/checkin/", methods=["POST"])
def add_customer():
    data = request.get_json()

    room_code = data["room_code"]
    customer_name = data["customer_name"]

    current = int(db.get(f"room:{room_code}:current"))
    total = int(db.get(f"room:{room_code}:total"))
    avail = int(db.get(f"room:{room_code}:avail"))

    if total == current:
        return {"message": "You can't check in this room"}

    current += 1

    if total == current:
        avail = 0
        event = {"room_code": room_code,
                 "total": total,
                 "current": current,
                 "avail": avail}
    else:
        event = {"room_code": room_code,
                 "total": total,
                 "current": current,
                 "avail": avail}

    db.sadd(f"room:{room_code}:customers", customer_name)
    db.sadd("customers", f"{customer_name}_{room_code}")

    db.set(f"room:{room_code}:avail", event["avail"])
    db.set(f"room:{room_code}:current", event["current"])

    return {"message": f"{customer_name} checked in"}


@bp.route("/checkout/", methods=["POST"])
def remove_customer():
    data = request.get_json()

    room_code = data["room_code"]
    customer_name = data["customer_name"]

    if db.sismember(f"room:{room_code}:customers", customer_name) != 1:
        return "there is an error regarding member name or room code"
    else:
        current = int(db.get(f"room:{room_code}:current"))

        db.srem(f"room:{room_code}:customers", customer_name)
        db.srem("customers", f"{customer_name}_{room_code}")

        current -= 1

        db.set(f"room:{room_code}:avail", 1)
        db.set(f"room:{room_code}:current", current)

        return {"message": f"{customer_name} checked out"}


@bp.route("/rooms/", methods=["GET"])
def room_list():
    result = db.smembers("rooms")
    result_list = list(result)
    output = {}
    i = 1
    for item in range(0, len(result_list)):
        output[f"room {i}"] = item
        i += 1
    return output


@bp.route("/customers/", methods=["GET"])
def customer_list():
    result = db.smembers("customers")
    result_list = list(result)
    output = {}
    i = 1
    for item in range(0, len(result_list)):
        output[f"room {i}"] = item
        i += 1
    return output
