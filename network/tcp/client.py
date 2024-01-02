from protocol import Client

client = Client()

client.add_methods({})


def main():
    with client:
        while True:
            data = input("Enter Command: ")

            if data.split()[0].lower() == "exit":
                break

            if client.validate_input(data):
                print(client.send_msg(data))
            else:
                print("Invalid Input")


if __name__ == "__main__":
    main()
