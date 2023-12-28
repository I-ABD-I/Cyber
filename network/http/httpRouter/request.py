import json
from socket import socket
from typing import Any


class InvalidRequestError(Exception):
    ...


class Request:
    request: bytes
    method: str
    url: str
    headers: dict[str, str]
    raw_data: bytes
    json: Any
    params: dict[str, str]
    cookies: dict[str, str]
    sock: socket

    def __init__(self, sock: socket):
        self.sock = sock
        self.request = self.sock.recv(1024)

        if not self.is_valid():
            raise InvalidRequestError("Invalid request")

        self.method = self.parse_method()
        self.url = self.parse_url()
        self.headers = self.parse_headers()
        self.raw_data = self.parse_raw_data()
        self.json = self.parse_json()
        self.params = self.parse_params()
        self.cookies = self.parse_cookies()

        print(f"{self.method} {self.url}")

    def parse_headers(self) -> dict[str, str]:
        lst = [
            str(header).split(":", 1)
            for header in self.request.split(b"\r\n\r\n")[0].split(b"\r\n")[1:]
        ]
        return dict(lst)

    def parse_method(self) -> str:
        return self.request.split(b" ")[0].decode()

    def parse_url(self) -> str:
        return self.request.split(b" ")[1].decode()

    def parse_raw_data(self) -> bytes:
        return self.request.split(b"\r\n\r\n")[1]

    def parse_json(self) -> Any:
        try:
            if self.headers.get("Content-Type") == "application/json":
                return json.loads(self.raw_data)
        except:
            pass
        return None

    def parse_params(self) -> dict[str, str]:
        self.url, params = self.url.split("?") if "?" in self.url else (self.url, "")
        return dict([param.split("=") for param in params.split("&")]) if params else {}

    def parse_cookies(self) -> dict[str, str]:
        cookies = self.headers.get("Cookie")
        if cookies is None:
            return {}

        return dict([cookie.split("=") for cookie in cookies.split(";")])

    def is_valid(self) -> bool:
        try:
            method, url, version = self.request.split(b"\r\n")[0].split(b" ", 3)
            return method in {
                b"GET",
                b"POST",
                b"PUT",
                b"DELETE",
                b"PATCH",
                b"HEAD",
                b"OPTIONS",
                b"TRACE",
                b"CONNECT",
            }
        except:
            return False
