from socket import AF_INET, SOCK_STREAM, socket


with socket(AF_INET, SOCK_STREAM) as s:
    s.connect(("172.16.13.122", 8820))
    s.send(b"Name")
    data = s.recv(1024)
    print(data.decode())
