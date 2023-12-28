from enum import Enum
from socket import socket

from .http_status_code import HttpStatusCode


class Response:
    code: HttpStatusCode
    headers: dict[str, str]
    data: bytes
    cookies: dict[str, str]

    def __init__(
        self,
        code: HttpStatusCode = HttpStatusCode.OK,
        headers: dict[str, str] = {"Content-Type": "text/plain; charset=utf-8"},
        data: bytes = b"",
        cookies: dict[str, str] = {},
    ):
        self.code = code
        self.headers = headers
        self.data = data
        self.cookies = cookies

    def __bytes__(self) -> bytes:
        prefix = f"HTTP/1.1 {self.code.value} {self.code.name.replace("_", " ").title()}\r\n".encode()
        self.add_header("Content-Length", str(len(self.data)))
        headers = "".join([f"{key}: {value}\r\n" for key, value in self.headers.items()]).encode()
        cookies = "".join([f"Set-Cookie: {key}={value}\r\n" for key, value in self.cookies.items()]).encode()
        return prefix + headers + cookies + b"\r\n" + self.data

    def add_header(self, key: str, value: str) -> None:
        self.headers[key] = value
