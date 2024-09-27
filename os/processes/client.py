"""
Written By : Aylon
Date       : 21 / 09 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Imports -------------------
import socket
from sys import stderr
from typing import Iterable

import wmi

# endregion


def send_proc_list(socket: socket.socket):
    _wmi = wmi.WMI()
    processes: Iterable[wmi._wmi_object] = _wmi.Win32_Process()

    for process in processes:
        socket.send(f"{process.ProcessId:>10} | {process.Name}".encode())


# region ------------------- Main -------------------
def main():
    sock = socket.socket()
    try:
        sock.connect(("127.0.0.1", 0x1ABD))
    except socket.error as e:
        print(e, file=stderr)

    main_loop = True
    while main_loop:
        try:
            msg = sock.recv(1024)
            if msg == b"send":
                send_proc_list(sock)
        except socket.error as e:
            print(e, file=stderr)
            main_loop = False


# endregion


if __name__ == "__main__":
    main()
