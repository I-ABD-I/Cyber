"""EX 2.6 protocol implementation
   Author:
   Date:
"""

import datetime
from random import randint
from socket import socket


LENGTH_FIELD_SIZE = 2
PORT = 8820

commands = {
    "RAND": lambda: randint(1, 10),
    "NAME": lambda: "SERVER2.6",
    "TIME": lambda: datetime.time(),
    "EXIT": lambda: "EXIT",
}


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    return data in commands


def create_msg(data):
    """Create a valid protocol message, with length field"""
    return f"{len(str(data)):02d}{data}".encode()


def get_msg(my_socket: socket):
    """Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error" """
    data = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if data.isnumeric():
        data = my_socket.recv(int(data)).decode()
        return True, data

    return False, "Error"
