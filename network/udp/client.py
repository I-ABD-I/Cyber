import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with sock:
        sock.sendto("world".encode(), ("127.0.0.1", 8820))
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data.decode()} from {addr}")


if __name__ == "__main__":
    main()
