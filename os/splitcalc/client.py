import hashlib
import multiprocessing
import os
import socket

import protodef


class Client:
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.sock.connect(("127.0.0.1", 8080))
        self.target = None

    def on_connect(self):
        protodef.send_packet(self.sock, protodef.Request(os.cpu_count()))

    def handle(self, packet):
        match packet:
            case protodef.Target:
                self.target = packet.target
            case protodef.Range:
                if not self.target:
                    raise Exception()

                start = packet.start
                end = packet.end
                cpus = os.cpu_count()
                with multiprocessing.Pool(
                    cpus,
                ) as pool:
                    if any(
                        res := pool.map(
                            self.hash_cracker,
                            (
                                range(s, s + (end - start) / cpus)
                                for s in range(start, end, (end - start) / cpus)
                            ),
                        )
                    ):
                        protodef.send_packet(
                            self.sock, protodef.Found(filter(lambda a: a, res))
                        )

    def hash_cracker(self, range):
        for i in range:
            hash = hashlib.md5(str(i).zfill(10).encode()).hexdigest()
            if hash == self.target:
                return i
        return False
