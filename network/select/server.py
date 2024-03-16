import socket
import select


MAX_MSG_LENGTH = 1024
SERVER_PORT = 0x1ABD
SERVER_IP = "0.0.0.0"


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.listen()

    open_client_sockets = []
    messages_to_send = []
    while True:
        rlist, wlist, xlist = select.select(
            [server_sock] + open_client_sockets, open_client_sockets, []
        )
        for sock in rlist:
            if sock is server_sock:
                new_sock, _ = server_sock.accept()
                open_client_sockets.append(new_sock)
                continue
            data = sock.recv(MAX_MSG_LENGTH)

            if not data:
                print("Connection closed")
                open_client_sockets.remove(sock)
                continue
            else:
                messages_to_send.append((sock, data))
        for sock, data in messages_to_send:
            if sock in wlist:
                sock.send(data)
                messages_to_send.remove((sock, data))


if __name__ == "__main__":
    main()
