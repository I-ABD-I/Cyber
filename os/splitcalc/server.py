import hashlib
import io
import queue
import socket
import threading
from typing import Iterator

import protodef

TARGET_MD5 = "EC9C0F7EDCC18A98B1F31853B1813301"
BLOCKSIZE = 10**6


class Server:
    def __init__(self) -> None:
        self.sock = socket.socket()
        self.sock.bind(("0.0.0.0", 8080))

    def run(self):
        self.sock.listen()

        it = iter(range(3689000000, 10**11, BLOCKSIZE))
        self.sock.setblocking(False)
        threads: list[ClientHandler] = []
        while True:
            try:
                sock, _ = self.sock.accept()
                sock.setblocking(True)
                ch = ClientHandler(sock, it, queue.Queue(), queue.Queue())
                ch.start()
                threads.append(ch)
            except socket.error:
                msg = None
                for thread in threads:
                    if not thread.outq.empty():
                        msg = thread.outq.get()
                if msg:
                    for thread in threads:
                        thread.inq.put(msg)
                    break

        for thread in threads:
            thread.join()


iterlock = threading.Lock()


class ClientHandler(threading.Thread):
    def __init__(
        self,
        sock: socket.socket,
        it: Iterator[int],
        inq: queue.Queue,
        outq: queue.Queue,
    ) -> None:
        threading.Thread.__init__(self)
        self.sock = sock
        self.iter = it
        self.inq = inq
        self.outq = outq

    def recv(self):
        length = int.from_bytes(self.sock.recv(2), byteorder="big")
        data = self.sock.recv(length)
        cls = protodef.server_ids[data[0]]
        return cls.unpack(data[1:])

    def on_req(self, pkt: protodef.Request):
        threads = pkt.cores
        with iterlock:
            start = next(self.iter)
            for _ in range(threads):
                next(self.iter)
        end = start + BLOCKSIZE * threads

        protodef.send_packet(self.sock, protodef.Range(start, end))

    def run(self):
        protodef.send_packet(self.sock, protodef.Target(TARGET_MD5))
        pkt = self.recv()

        if not isinstance(pkt, protodef.Request):
            return

        self.on_req(pkt)

        while True:
            if not self.inq.empty():
                msg = self.inq.get()
                protodef.send_packet(self.sock, msg)
                if isinstance(msg, protodef.Quit):
                    return

            pkt = self.recv()
            match pkt:
                case protodef.Request():
                    self.on_req(pkt)
                case protodef.Found():
                    if hashlib.md5(pkt.hash.encode()):
                        print(f"Found: {pkt.hash}, {TARGET_MD5}")
                        self.outq.put(msg := protodef.Quit())
                        protodef.send_packet(self.sock, msg)
                        return
                case _:
                    self.sock.close()
                    return


def main():
    serv = Server()
    serv.run()


if __name__ == "__main__":
    main()
