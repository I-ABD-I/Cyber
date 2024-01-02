import socket
from . import shared


class Client:
    sock: socket.socket
    methods: dict[str, tuple[int, bool]]

    def __init__(self, host: str = "localhost", port: int = None):  # type: ignore
        if port is None:
            port = shared.PORT

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.methods = {}

    def send_msg(self, msg: str) -> str:
        self.sock.sendall(shared.create_msg(msg).encode())
        return shared.get_msg(self.sock.recv(1024).decode())

    def validate_input(self, msg: str) -> bool:
        lst = msg.lower().split()

        if lst[0] not in self.methods:
            return False

        if self.methods[lst[0]][1]:
            return (len(lst) - 1) == self.methods[lst[0]][0]

        return (len(lst) - 1) >= self.methods[lst[0]][0]

    def add_method(self, method: str, args: int, fixed: bool):
        self.methods[method] = (args, fixed)

    def add_methods(self, methods: dict[str, tuple[int, bool]]):
        self.methods.update(methods)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.sock.__exit__(*args)
