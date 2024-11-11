"""
Written By : Aylon
Date       : 4 / 11 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

import glob
import os
import socket

from shared import EncSocketWrapper


def main():
    sock = EncSocketWrapper(socket.socket())
    sock.connect("127.0.0.1", 8080)

    cdir_list = (d for d in glob.glob("c:/*") if os.path.isdir(d))
    sock.send("\n".join(cdir_list).encode())

    dir1 = sock.recv(1024).decode()
    filelist = glob.glob(f"c:/{dir1}/*")
    sock.send("\n".join(filelist).encode())


if __name__ == "__main__":
    main()
