import io
import socket
import threading

import protodef

TARGET_MD5 = "EC9COF7EDCC18A98B1F31853B1813301"


class Server:
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0", 8080))

    def run(self):
        self.sock.listen()

        while True:
            sock, addr = self.sock.accept()


class ClientHandler(threading.Thread):
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.read = io.BufferedReader(sock.makefile("rb"))  # type: ignore

    def recv(self):
        self.read.read(1)

    def run(self):

        while True:
            ...
