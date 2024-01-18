PORT = 5000
LENGTH_FIELD_SIZE = 4


def init(port: int = 5000, length_field_size: int = 4):
    global PORT, LENGTH_FIELD_SIZE
    PORT = port
    LENGTH_FIELD_SIZE = length_field_size


def create_msg(msg: str) -> str:
    return f"{len(msg):0{LENGTH_FIELD_SIZE}d}{msg}"


def get_msg(msg: str) -> str:
    return msg[LENGTH_FIELD_SIZE: int(msg[:LENGTH_FIELD_SIZE]) + LENGTH_FIELD_SIZE]
