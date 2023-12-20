#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import os
import socket
import protocol


IP = "127.0.0.1"
SAVED_PHOTO_LOCATION = "C:/python/School/cyber/class/network/ex2.7/cache/client/screenshot.jpg"  # The path + filename where the copy of the screenshot at the client should be saved


def handle_server_response(my_socket: socket.socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    if cmd.split()[0].upper() in {
        "DIR",
        "DELETE",
        "COPY",
        "EXECUTE",
        "TAKE_SCREENSHOT",
        "EXIT",
    }:
        valid, data = protocol.get_msg(my_socket)
        print(data if valid else "Error")
    # (10) treat SEND_PHOTO

    if cmd.split()[0].upper() == "SEND_PHOTO":
        valid, data = protocol.get_msg(my_socket)
        if valid:
            os.makedirs(os.path.dirname(SAVED_PHOTO_LOCATION), exist_ok=True)
            if not data.isnumeric():
                return
            length = int(data)
            with open(SAVED_PHOTO_LOCATION, "wb") as f:
                recv_bytes = 0
                while recv_bytes < length:
                    chunk = my_socket.recv(1024)
                    if chunk:
                        f.write(chunk)
                        recv_bytes += len(chunk)


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol.PORT))
    # (2)

    # print instructions
    print("Welcome to remote computer application. Available commands are:\n")
    print("TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT")

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet.encode())
            handle_server_response(my_socket, cmd)
            if cmd.upper() == "EXIT":
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == "__main__":
    main()
