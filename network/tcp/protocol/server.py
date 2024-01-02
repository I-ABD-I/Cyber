import socket
from typing import Callable, Protocol

from . import shared


class Server:
    """Server class"""

    sock: socket.socket
    methods: dict[str, Callable[[list], str]]
    validators: dict[str, Callable[[list], bool]]

    def __init__(self, port: int = None, host: str = "0.0.0.0"):  # type: ignore
        if port is None:
            port = shared.PORT

        self.methods = {}
        self.validators = {}

        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def add_method(self, method: str, param_count: int = 0, fixed: bool = True):
        method = method.lower()

        def decotator(func: Callable[[list], str]):
            self.methods[method] = func
            self.methods[method].param_count = param_count
            self.methods[method].fixed = fixed
            return func

        return decotator

    def add_validator(self, method: str):
        method = method.lower()

        def decotator(func: Callable[[list], bool]):
            self.validators[method] = func
            return func

        return decotator

    def decode_msg(self, msg: str) -> tuple[str, list[str]]:
        method, *args = msg.strip().split(" ")
        return method, args

    def get_msg(self, data: str):
        return shared.get_msg(data)

    def send_msg(self, msg: str, conn: socket.socket):
        conn.sendall(shared.create_msg(msg).encode())

    def validate_request(self, method: str, args: list[str]) -> bool:
        if method not in self.methods:
            return False

        valid = True
        if self.validators.get(method):
            valid = self.validators[method](args)

        if self.methods[method].fixed:
            return valid and len(args) == self.methods[method].param_count
        return valid and len(args) >= self.methods[method].param_count

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.sock.__exit__(args)
