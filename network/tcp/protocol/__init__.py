from . import shared
from .server import Server
from .client import Client


def init(port: int = 5000, length_field_size: int = 4):
    shared.init(port, length_field_size)
