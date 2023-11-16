import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

url = "7.tcp.eu.ngrok.io:17476"
host, port = url.split(":")
s.connect((host, int(port)))

s.send("Aylon".encode())

print(s.recv(1024).decode())

s.close()
