#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import glob
import os
import shutil
import socket
import subprocess
import protocol
import pyautogui


IP = "0.0.0.0"
PHOTO_PATH = "C:/python/School/cyber/class/network/ex2.7/cache/server/screenshot.jpg"  # The path + filename where the screenshot at the server should be saved


def cmd_DIR(params):
    return "\n".join(glob.glob((params[0] + "/*")))


def cmd_DELETE(params):
    try:
        os.remove(params[0])
        return f"DELETED {params[0]}"
    except Exception as e:
        return e


def cmd_COPY(params):
    try:
        shutil.copy(params[0], params[1])
        return f"Copied {params[0]} to {params[1]}"
    except Exception as e:
        return e


def cmd_EXECUTE(params):
    try:
        return subprocess.call(params)
    except Exception as e:
        return e


def cmd_SCREENSHOT(params):
    try:
        os.makedirs(os.path.dirname(p=PHOTO_PATH), exist_ok=True)
        pyautogui.screenshot().save(PHOTO_PATH)
        return "Successfully took screenshot"
    except:
        return "Failed to take screenshot"


def cmd_SENDPHOTO(params):
    try:
        return str(os.path.getsize(PHOTO_PATH))
    except Exception as e:
        return e


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    if protocol.check_cmd(cmd):
        params = cmd.split()[1:]
        match cmd := cmd.split()[0].upper():
            case "EXIT" | "TAKE_SCREENSHOT" | "SEND_PHOTO":
                return len(params) == 0, cmd, params
            case "DIR":
                return len(params) == 1, cmd, params
            case "COPY":
                return (
                    len(params) == 2 and os.path.isfile(params[0]),
                    cmd,
                    params,
                )
            case "DELETE":
                return (
                    len(params) == 1 and os.path.isfile(params[0]),
                    cmd,
                    params,
                )
            case "EXECUTE":
                return (
                    (len(params) >= 1 and shutil.which(params[0])) is not None,
                    cmd,
                    params,
                )

    return False, "ERROR", []


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """

    cmds = {
        "DIR": cmd_DIR,
        "DELETE": cmd_DELETE,
        "COPY": cmd_COPY,
        "EXECUTE": cmd_EXECUTE,
        "EXIT": lambda _: "Exiting",
        "TAKE_SCREENSHOT": cmd_SCREENSHOT,
        "SEND_PHOTO": cmd_SENDPHOTO,
    }
    # (7)

    response = cmds[command](params)
    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen(1)
    # (1)
    client_socket, addr = server_socket.accept()
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                response = handle_client_request(command, params)
                # prepare a response using "handle_client_request"

                # add length field using "create_msg"
                response = protocol.create_msg(response)
                # send to client
                client_socket.send(response.encode())
                if command == "SEND_PHOTO":
                    # Send the data itself to the client
                    with open(PHOTO_PATH, "rb") as f:
                        while readbytes := f.read(1024):
                            client_socket.send(readbytes)

                if command == "EXIT":
                    break
            else:
                # prepare proper error to client
                response = "Bad command or parameters"
                # send to client
                client_socket.send(response.encode())

        else:
            # prepare proper error to client
            response = "Packet not according to protocol"
            # send to client
            client_socket.send(response.encode())
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
