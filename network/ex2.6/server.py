"""EX 2.6 server implementation
   Author:
   Date:
"""

import socket
import protocol


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    return protocol.commands[cmd.upper()]()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            # 2. Check if the command is valid
            # 3. If valid command - create response
            print(cmd)
            if protocol.check_cmd(cmd):
                response = create_server_rsp(cmd)
                client_socket.send(protocol.create_msg(response))
                if response == "EXIT":
                    break
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(
                1024
            )  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client

        # Send response to the client

    print("Closing\n")
    # Close sockets


if __name__ == "__main__":
    main()
