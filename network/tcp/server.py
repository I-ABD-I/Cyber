import socket

from protocol import Server

server = Server()


def handle_conn(conn: socket.socket):
    while True:
        try:
            data = conn.recv(1024)
        except socket.error:
            break

        if not data:
            break

        data = server.get_msg(data.decode())
        method, args = server.decode_msg(data.lower())

        if method == "exit":
            break

        if not server.validate_request(method, args):
            server.send_msg("Invalid Request", conn)
            continue

        server.send_msg(server(method, args), conn)


def main():
    with server:
        while True:
            conn, addr = server.sock.accept()
            print("Client Connected", addr)
            with conn:
                handle_conn(conn)


if __name__ == "__main__":
    main()
