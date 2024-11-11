import abc
import socket
import struct
from abc import abstractmethod

client_ids = {}

ids = [0, 0]


def clientbound(fmt):
    def decorator(clas: type):
        clas.struct = struct.Struct(fmt)
        clas.id = ids[0]
        ids[0] += 1
        client_ids[clas.id] = clas
        return clas

    return decorator


server_ids = {}


def serverbound(fmt):
    def decorator(clas: type):
        clas.struct = struct.Struct(fmt)
        clas.id = ids[1]
        ids[1] += 1
        server_ids[clas.id] = clas
        return clas

    return decorator


def send_packet(socket: socket.socket, data: "Packet"):
    bts = data.pack()
    bts = struct.pack("!hs", len(bts), data)
    # socket.send(data)


class Packet(abc.ABC):
    @abstractmethod
    def pack(self):
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def unpack(data):
        raise NotImplemented


@serverbound("!h")
class Request(Packet):
    """class defines the first message of amnt of client sys threads"""

    def __init__(self, cores) -> None:
        self.cores = cores

    def pack(self):
        return Request.struct.pack(self.cores)

    @staticmethod
    def unpack(data):
        Request(*Request.struct.unpack(data))


@clientbound("!pp")
class Range(Packet):
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def pack(self):
        return Range.struct.pack(self.start, self.end)

    @staticmethod
    def unpack(data):
        return Range(*Range.struct.unpack(data))


@clientbound("!32s")
class Target(Packet):
    def __init__(self, target) -> None:
        self.target = target

    def pack(self):
        return Target.struct.pack(self, self.target)

    @staticmethod
    def unpack(data):
        return Target(*Target.struct.unpack(data))


@serverbound("!10s")
class Found(Packet):
    def __init__(self, hash):
        self.hash = hash

    def pack(self):
        return Found.struct.pack(self.hash)

    @staticmethod
    def unpack(data):
        return Found(*Found.struct.unpack())
