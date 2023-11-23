"""EX 2.6 client implementation
   Author:
   Date:
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        valid_cmd = protocol.check_cmd(user_input)

        if valid_cmd:
            # If the command is valid:
            # 1. Add length field ("RAND" -> "04RAND")
            # 2. Send it to the server
            # 3. If command is EXIT, break from while loop
            # 4. Get server's response
            # 5. If server's response is valid, print it

            msg = protocol.create_msg(user_input)
            my_socket.send(msg)
            if user_input == "EXIT":
                break
            valid, response = protocol.get_msg(my_socket)

            if valid:
                print(response)

            else:
                print("Response not valid\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    # Close socket


if __name__ == "__main__":
    main()
