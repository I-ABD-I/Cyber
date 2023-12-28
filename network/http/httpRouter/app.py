import socket
from .request import InvalidRequestError, Request
from .router import Router


class HTTPServer:
    def __init__(self, port=80, default_gateway="/index.html", file_server="./"):
        self.port = port
        self.router = Router(default_gateway, file_server)

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", self.port))
        sock.listen()
        print(f"Listening for connections on port {self.port}...")
        while True:
            client_socket, _ = sock.accept()
            client_socket.settimeout(0.1)

            try:
                req = Request(client_socket)
                self.router.handle(req)
            except (socket.timeout, InvalidRequestError) as e:
                print(e)
            client_socket.close()

    def get(self, path: str):
        return self.router.get(path)

    def post(self, path: str):
        return self.router.post(path)

    def put(self, path: str):
        return self.router.put(path)

    def delete(self, path: str):
        return self.router.delete(path)

    def static(self, path: str):
        return self.router.static(path)
