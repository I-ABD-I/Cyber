from typing import Callable
from .http_status_code import HttpStatusCode
from .request import Request
from .response import Response
import os


class Route:
    path: str
    methods: dict[str, Callable]
    is_static: bool

    def __init__(
        self,
        path: str,
        methods: dict[str, Callable[[Request], Response]] = {},
        is_static: bool = False,
        file_server: str = ".",
    ):
        self.path = path
        self.methods = methods
        self.is_static = is_static
        self.file_server = file_server.removesuffix("/")

        if self.is_static:
            self.methods["GET"] = self.GET_static

    def GET_static(self, request: Request) -> Response:
        url = request.url.split("?")[0]

        try:
            with open(f"{self.file_server}{url}", "rb") as f:
                data = f.read()
        except FileNotFoundError:
            return Response(
                code=HttpStatusCode.NOT_FOUND,
            )
        return Response(data=data, headers={"Content-Type": get_content_type(url)})


def get_content_type(filename: str) -> str:
    # Mapping of file extensions to MIME types
    MIME_TYPES = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
    }
    _, file_extension = os.path.splitext(filename)

    return MIME_TYPES.get(file_extension, "application/octet-stream")
