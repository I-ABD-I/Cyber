"""
Written By : Aylon
Date       : 21 / 09 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Imports -------------------
import socket
import threading
from sys import stderr

# endregion


# region ------------------- Globals -------------------
class Logger:
    def __init__(self) -> None:
        self.__lock = threading.Lock()

    def print(self, msg):
        with self.__lock:
            print(msg)


_logger = Logger()
# endregion


# region ------------------- Threads -------------------
class ClientThread(threading.Thread):
    def __init__(self, socket: socket.socket, server: "Server", id) -> None:
        threading.Thread.__init__(self)
        self.server = server
        self.socket = socket
        self.id = id

    def run(self):
        running = True
        while running:
            try:
                data = self.socket.recv(1024)
                _logger.print(data.decode())
            except socket.error as e:
                print(e, file=stderr)
                running = False
                del self.server.clients[self.id]


class Server(threading.Thread):
    def __init__(self, port) -> None:
        threading.Thread.__init__(self)
        self.port = port
        self.clients = {}

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
            listening_socket.bind(("0.0.0.0", self.port))

            listening_socket.listen()

            self.clients: dict[int, ClientThread] = {}
            id_gen = iter(range(0xFFFFFFFF))

            connection_loop = True
            while connection_loop:
                try:
                    sock, addr = listening_socket.accept()

                    _logger.print(f"Client {addr} connected")
                    thread = ClientThread(sock, self, next(id_gen))
                    self.clients[thread.id] = thread
                    thread.start()

                except Exception as e:
                    connection_loop = False
                    print(e, file=stderr)


# endregion


# region ------------------- Main -------------------
def main():
    server = Server(0x1ABD)
    server.start()

    main_loop = True
    while main_loop:
        try:
            msg = input()
            match msg:
                case "list":
                    for id, client in server.clients.items():
                        _logger.print(f"{id:>10} | {client.socket.getsockname()}")
                case _:
                    server.clients[int(msg)].socket.send(b"send")
        except Exception as e:
            print(e, file=stderr)
            main_loop = False


# endregion


if __name__ == "__main__":
    main()
