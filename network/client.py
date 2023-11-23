from socket import AF_INET, SOCK_STREAM, socket


with socket(AF_INET, SOCK_STREAM) as s:
    s.connect(("localhost", 5000))
    s.send(b"Aylon")
    data = s.recv(1024)
    print(data.decode())
