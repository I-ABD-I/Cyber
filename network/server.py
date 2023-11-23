from socket import AF_INET, SOCK_STREAM, socket


with socket(AF_INET, SOCK_STREAM) as s:
    s.bind(("0.0.0.0", 5000))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        print(data)
        conn.send(f"Hello, {data}".encode())
