CREATE_ROOMS_TABLE = (
    """CREATE TABLE IF NOT EXISTS rooms (room_code SERIAL PRIMARY KEY, total INTEGER,
     current INTEGER, avail INTEGER);"""
)
INSERT_ROOM_RETURN_ID = "INSERT INTO rooms (total, current, avail) VALUES (%s, %s, %s) RETURNING room_code;"

CREATE_CUSTOMER_TABLE = """CREATE TABLE IF NOT EXISTS customers (customer_name TEXT, room_code INTEGER,
                        FOREIGN KEY(room_code) REFERENCES rooms(room_code) ON DELETE CASCADE);"""

INSERT_CUSTOMER = (
    "INSERT INTO customers (customer_name, room_code) VALUES (%s, %s);"
)

GET_CUSTOMERS = (
    "SELECT * FROM customers"
)

REMOVE_CUSTOMERS = (
    "DELETE FROM customers WHERE room_code = (%s) AND customer_name = (%s)"
)

GET_ROOMS = (
    "SELECT * FROM rooms"
)

# 고객이 입장한 room의 id 받아오는 select 구문 하나
GET_ROOM_ID = (
    "SELECT * FROM customers WHERE room_code = (%s);"
)
# 그 받아온 room id로 room 객체 선택하는 구문 하나
GET_ROOM_WITH_ID = (
    "SELECT * FROM rooms WHERE room_code = (%s);"
)
# 선택된 객체의 current 인자를 update시키는 구문 둘
CHANGE_CURRENT_ADD = (
    """UPDATE rooms
    SET current = current + 1
    WHERE room_code = (%s);"""
)

CHANGE_CURRENT_DELETE = (
    """UPDATE rooms
    SET current = current - 1
    WHERE room_code = (%s);"""
)


# current와 total이 같을 경우 availability를 update하는 구문 하나
CHANGE_AVAILABILITY_FALSE = (
    """UPDATE rooms
    SET avail = NULL
    WHERE room_code = (%s);"""
)

CHANGE_AVAILABILITY_TRUE = (
    """UPDATE rooms
    SET avail = 1
    WHERE room_code = (%s);"""
)
