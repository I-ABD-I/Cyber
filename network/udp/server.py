import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with sock:
        sock.bind(("0.0.0.0", 8820))
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data.decode()} from {addr}")
        sock.sendto(f"hello {data.decode()}".encode(), addr)


if __name__ == "__main__":
    main()
