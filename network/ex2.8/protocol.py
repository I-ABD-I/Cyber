from socket import AF_INET, SOCK_STREAM, socket


LENGTH_FIELD_SIZE = 4


def listen_on_port(port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(("0.0.0.0", port))
    sock.listen(1)
    print("Listening on port", sock.getsockname()[1])
    return sock


def connect_to_port(addr, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((addr, port))
    print(f"Connected to {addr}:{port}")
    return sock


def create_msg(data, next_port):
    return f"{len(data):0{LENGTH_FIELD_SIZE}d}{data}{next_port:05d}".encode()


def get_msg(sock: socket):
    data = sock.recv(1024).decode()
    if (msg_len := data[:LENGTH_FIELD_SIZE]).isnumeric():
        return (
            True,
            data[LENGTH_FIELD_SIZE : int(msg_len) + LENGTH_FIELD_SIZE],
            data[int(msg_len) + LENGTH_FIELD_SIZE :],  # next port
        )
    return False, "ERROR", 0
