from protocol import connect_to_port, create_msg, get_msg, listen_on_port


def main():
    # connect to server on port 8000
    client_socket = connect_to_port("127.0.0.1", 8000)
    while True:
        # listen on a random dynamic port
        sock = listen_on_port(0)
        with client_socket, sock:
            # send message with the random port
            msg = input("Enter Message: ")
            client_socket.send(create_msg(msg, sock.getsockname()[1]))
            if msg == "exit":
                break

            # get message sent and break if exit
            client_socket, addr = sock.accept()
            valid, msg, next_port = get_msg(client_socket)
            if valid:
                print(f"Recived: {msg}")
                if msg == "exit":
                    break

        # connect to the next port that was send before
        client_socket = connect_to_port(addr[0], int(next_port))


if __name__ == "__main__":
    main()
