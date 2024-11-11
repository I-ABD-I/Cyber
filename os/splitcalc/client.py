import hashlib
import io
import multiprocessing
import os
import socket

import protodef


class Client:
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.sock.connect(("127.0.0.1", 8080))
        self.target = None

    def recv(self):
        # t = self.read.read(2)
        length = int.from_bytes(self.sock.recv(2), byteorder="big")
        data = self.sock.recv(length)
        cls = protodef.client_ids[data[0]]
        return cls.unpack(data[1:])

    def on_connect(self):
        target = self.recv()
        self.target = target.target.lower()
        protodef.send_packet(self.sock, protodef.Request(os.cpu_count()))  # type: ignore

    def handle(self, packet):
        match packet:
            case protodef.Quit():
                print("Hash was found quitting...")
                exit()
            case protodef.Target():
                self.target = packet.target.lower()
            case protodef.Range():
                if not self.target:
                    raise Exception()

                start = packet.start
                end = packet.end
                print(f"Processsing {start} -> {end}")
                cpus = os.cpu_count()
                with multiprocessing.Pool(
                    cpus,
                ) as pool:
                    if any(
                        res := pool.map(
                            self.hash_cracker,
                            (
                                range(s, s + (end - start + 1) // cpus)
                                for s in range(start, end, (end - start + 1) // cpus)
                            ),
                        )
                    ):
                        protodef.send_packet(
                            self.sock,
                            protodef.Found(
                                str(next(filter(lambda a: a, res))).zfill(10)
                            ),
                        )
                    else:
                        protodef.send_packet(self.sock, protodef.Request(cpus))  # type: ignore
                    print(res)

    def hash_cracker(self, range):
        for i in range:
            hash = hashlib.md5(str(i).zfill(10).encode()).hexdigest()
            if hash == self.target:
                return i
        return False


def main():
    client = Client()
    client.on_connect()
    while True:
        client.handle(client.recv())


if __name__ == "__main__":
    main()
