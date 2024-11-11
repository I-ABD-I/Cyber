"""
Written By : Aylon
Date       : 4 / 11 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

import socket

from shared import EncSocketWrapper


def main():
    listening = EncSocketWrapper(socket.socket())
    listening.bind("0.0.0.0", 8080)
    listening.listen()
    sock, _ = listening.accept()
    print(sock.recv(2048).decode())
    dir = input("please enter a directory")

    sock.send(dir.encode())
    print(sock.recv(2048).decode())


if __name__ == "__main__":
    main()
