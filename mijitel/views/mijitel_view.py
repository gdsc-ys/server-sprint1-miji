from flask import Blueprint, request
from werkzeug.utils import redirect
import psycopg2
import os
from ..sql.sql_commands import *

bp = Blueprint('mijitel', __name__, url_prefix='/')

url = os.environ.get("DATABASE_URL")  # gets variables from environment
connection = psycopg2.connect(url)


# {"total": "#", "current": "#"}
@bp.route("/room/", methods=["POST"])
def create_room():
    data = request.get_json()
    total = data["total"]
    current = data["current"]
    avail = data["avail"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(INSERT_ROOM_RETURN_ID, (total, current, avail))
            room_code = cursor.fetchone()[0]
    if avail:
        return {"id": room_code, "message": f"Room {room_code} {current}/{total} is available."}
    else:
        return {"id": room_code, "message": f"Room {room_code} {current}/{total} is not available."}


# {"customer_name": "~~", "room_code": 1}
@bp.route("/checkin/", methods=["POST"])
def add_customer():
    data = request.get_json()
    room_code = data["room_code"]
    customer_name = data["customer_name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ROOMS, (room_code,))
            room = cursor.fetchall()[0]
            room_total = room[1]
            room_current = room[2]
            if room_total == room_current:
                return {"message": "You can't check in this room"}
            cursor.execute(CREATE_CUSTOMER_TABLE)
            cursor.execute(INSERT_CUSTOMER, (customer_name, room_code))
            cursor.execute(CHANGE_CURRENT_ADD, (room_code,))

            cursor.execute(GET_ROOMS, (room_code,))
            room = cursor.fetchall()[0]
            room_total = room[1]
            room_current = room[2]
            if room_total == room_current:
                cursor.execute(CHANGE_AVAILABILITY_FALSE, (room_code, ))
    return {"message": f"{customer_name} checked in"}


@bp.route("/rooms/", methods=["GET"])
def room_list():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_ROOMS)
            results = cursor.fetchall()

    return {"message": results}


@bp.route("/customers/", methods=["GET"])
def customer_list():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_CUSTOMERS)
            results = cursor.fetchall()

    return {"message": results}


# {"customer_name": "~~", "room_code": 1}
@bp.route("/checkout/", methods=["POST"])
def remove_customer():

    data = request.get_json()
    room_code = data["room_code"]
    customer_name = data["customer_name"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(REMOVE_CUSTOMERS, (room_code, customer_name))
            cursor.execute(CHANGE_CURRENT_DELETE, (room_code,))
            cursor.execute(CHANGE_AVAILABILITY_TRUE, (room_code, ))

    return {"message": f"{customer_name} checked out from {room_code} room"}



