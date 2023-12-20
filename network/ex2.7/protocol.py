#   Ex. 2.7 template - protocol


from socket import socket


LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(cmd: str):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\\work\\file.txt is good, but DELETE alone is not
    """
    cmd, params = cmd.split()[0], cmd.split()[1:]

    match cmd.upper():
        case "EXIT" | "TAKE_SCREENSHOT" | "SEND_PHOTO":
            return len(params) == 0
        case "DIR" | "DELETE":
            return len(params) == 1
        case "COPY":
            return len(params) == 2
        case "EXECUTE":
            return len(params) >= 1
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    return f"{len(str(data)):0{LENGTH_FIELD_SIZE}d}{data}"


def get_msg(my_socket: socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    data = my_socket.recv(1024).decode()
    if (length := data[:LENGTH_FIELD_SIZE]).isnumeric():
        return True, data[LENGTH_FIELD_SIZE : int(length) + LENGTH_FIELD_SIZE]

    return False, "Error"
