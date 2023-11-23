import socket

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(("serv.me", 0xABD))

serversocket.listen()
print("Server running")

conn, addr = serversocket.accept()
print(f"Connection from: {addr}")

name = conn.recv(1024).decode()
print(f"Received: {name}")

conn.send(f"Hello, {name}".encode())
print(f"Sent Hello, {name}")

conn.close()
serversocket.close()
