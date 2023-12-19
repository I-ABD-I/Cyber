from socket import AF_INET, SOCK_STREAM, socket

from protocol import connect_to_port, create_msg, get_msg, listen_on_port


def main():
    sock = listen_on_port(8000)  # listen on port 8000 to start
    while True:
        client_socket, addr = sock.accept()  # wait for connection
        with sock, client_socket:  # close sockets when done
            # get message sent and break if exit
            valid, msg, next_port = get_msg(client_socket)
            if valid:
                print(f"Recived: {msg}")
                if msg == "exit":
                    break
            # listen on a random dynamic port
            sock = listen_on_port(0)
            # connect to the next port that was send before
            client_socket = connect_to_port(addr[0], int(next_port))

            # send message with the random port
            msg = input("Enter message: ")
            client_socket.send(create_msg(msg, sock.getsockname()[1]))
            if msg == "exit":
                break


if __name__ == "__main__":
    main()
