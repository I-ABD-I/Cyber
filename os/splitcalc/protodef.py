import abc
import socket
import struct
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Type, TypeVar


class Packet(abc.ABC):
    struct: ClassVar[struct.Struct]
    id: ClassVar[int]

    @abstractmethod
    def pack(self):
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def unpack(data):
        raise NotImplemented


client_ids = {}

ids = [0, 0]

T = TypeVar("T", bound=Packet)


def clientbound(fmt):

    def decorator(clas: Type[T]) -> Type[T]:
        clas.struct = struct.Struct(fmt)
        clas.id = ids[0]
        ids[0] += 1
        client_ids[clas.id] = clas
        return clas

    return decorator


server_ids = {}


def serverbound(fmt):
    def decorator(clas: Type[T]) -> Type[T]:
        clas.struct = struct.Struct(fmt)
        clas.id = ids[1]
        ids[1] += 1
        server_ids[clas.id] = clas
        return clas

    return decorator


def send_packet(socket: socket.socket, data: "Packet"):
    bts = data.pack()
    bts = struct.pack("!hB", len(bts) + 1, data.__class__.id) + bts  # type: ignore
    socket.send(bts)


@serverbound("!h")
class Request(Packet):
    """class defines the first message of amnt of client sys threads"""

    def __init__(self, cores: int) -> None:
        self.cores = cores

    def pack(self):
        return Request.struct.pack(self.cores)

    @staticmethod
    def unpack(data):
        return Request(*Request.struct.unpack(data))


@clientbound("!qq")
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
    def __init__(self, target: str) -> None:
        self.target = target

    def pack(self):
        return Target.struct.pack(self.target.encode())

    @staticmethod
    def unpack(data):
        bts, *_ = Target.struct.unpack(data)
        return Target(bts.decode())  # type: ignore


@serverbound("!10s")
class Found(Packet):
    def __init__(self, hash: str):
        self.hash = hash

    def pack(self):
        return Found.struct.pack(self.hash.encode())

    @staticmethod
    def unpack(data):
        hs, *_ = Found.struct.unpack(data)
        return Found(hs.decode())


@clientbound("!")
class Quit(Packet):
    def __init__(self): ...

    def pack(self):
        return Quit.struct.pack()

    @staticmethod
    def unpack(data):
        return Quit(*Quit.struct.unpack(data))
