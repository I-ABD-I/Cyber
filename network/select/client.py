import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 0x1ABD))
    while True:
        sock.send(input("Enter a name: ").encode())
        data = sock.recv(1024)
        print(data.decode())
    sock.close()


if __name__ == "__main__":
    main()
