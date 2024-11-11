"""
Written By : Aylon
Date       : 16 / 10 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Imports -------------------
import re
import socket
import threading
from typing import Callable

# endregion


# region ------------------- Classes -------------------
class Server:
    def __init__(self, port) -> None:
        self.socket = socket.socket()
        try:
            self.socket.bind(("0.0.0.0", port))
        except socket.error as e:
            print(e)
            print(f"Unable to bind socket to port: {port}")
            exit(-1)

    def run(self):
        threads: list[threading.Thread] = []
        try:
            self.socket.listen()
            running = True
            while running:
                sock, addr = self.socket.accept()
                print(f"client with addr: {addr} connected!")
                handler = ClientHandler(sock)
                handler.start()
                threads.append(handler)
        except socket.error as e:
            print(e)

        for thread in threads:
            thread.join()


class ClientHandler(threading.Thread):
    def __init__(self, sock: socket.socket) -> None:
        threading.Thread.__init__(self)
        self.socket = sock

    def run(self) -> None:
        running = True
        while running:
            try:
                cmd = self.socket.recv(1024).decode()
            except socket.error:
                running = False
                break

            patterns: dict[str, Callable[..., str]] = {
                r"show my( established| listening)? connections": lambda attr: f"cmd@netstat -na@{attr.upper() if attr else ""}",
                r"trace route to (\S+)": lambda host: f"cmd@tracert {host}@",
                r"show my ip": lambda: r"cmd@ipconfig@(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])",
                r"test connection to (\S+)": lambda addr: f"cmd@ping {addr}@",
            }

            response = "N/A"
            for pattern, func in patterns.items():
                if match := re.match(pattern, cmd):
                    response = func(*match.groups())

            self.socket.send(response.encode())


# endregion


# region ------------------- Main -------------------
def main():
    server = Server(8080)
    server.run()


if __name__ == "__main__":
    main()

# endregion
