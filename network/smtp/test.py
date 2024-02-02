import socket
from base64 import b64encode, b64decode
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

MAIL = "abd@gmx.com"
IP = "172.16.12.186"
sock.connect(("172.16.13.48", 25))
print(sock.recv(1024))
sock.send(f"EHLO {MAIL}\r\n".encode())
print(sock.recv(1024).decode())

auth = f"AUTH LOGIN\r\n"

sock.send(auth.encode())
print(sock.recv(1024).decode())

sock.send(f"{MAIL}\r\n".encode())
print(sock.recv(1024).decode())
sock.send(f"pass\r\n".encode())
print(sock.recv(1024).decode())

sock.send(f"MAIL FROM: <{MAIL}>\r\n".encode())
print(sock.recv(1024).decode())

sock.send(b"RCPT TO: hi@gmx.ocm\r\n")
print(sock.recv(1024).decode())

# sock.send(b"DATA\r\n")
# print(sock.recv(1024).decode())

# sock.send(b"\r\n.\r\n")
sock.send("DATA\r\n".encode())
sock.send(b"Subject: test")
sock.send(b"TEST MSG")
sock.send(b"\r\n.\r\n")

print(sock.recv(1024).decode())
sock.send(b"QUIT\r\n")
print(sock.recv(1024).decode())
sock.close()
