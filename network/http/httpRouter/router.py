from typing import Callable
from .http_status_code import HttpStatusCode
from .request import Request
from .response import Response
from .route import Route


class Router:
    routes: list[Route]

    def __init__(self, default_gateway: str, file_server: str = "./"):
        self.routes = []
        self.static_routes = []
        self.default = default_gateway
        self.file_server = file_server

    def handle(self, request: Request) -> None:
        if request.url == "/":
            request.url = self.default

        route = self._get_route(request.url)
        if route:
            response = route.methods[request.method](request)
        else:
            response = Response(
                HttpStatusCode.NOT_FOUND,
            )
        request.sock.send(bytes(response))

    def _route(self, path: str, method, func, is_static: bool = False):
        route = self._get_route(path)
        if route is None:
            if is_static:
                route = Route(path, is_static=is_static, file_server=self.file_server)
                self.static_routes.append(route)
            else:
                route = Route(path, {method: func})
                self.routes.append(route)
        else:
            route.methods[method] = func

    def get(self, path: str):
        def decorator(func: Callable[[Request], Response]):
            return self._route(path, "GET", func)

        return decorator

    def post(self, path: str):
        def decorator(func):
            return self._route(path, "POST", func)

        return decorator

    def put(self, path: str):
        def decorator(func):
            return self._route(path, "PUT", func)

        return decorator

    def delete(self, path: str):
        def decorator(func):
            return self._route(path, "DELETE", func)

        return decorator

    def patch(self, path: str):
        def decorator(func):
            return self._route(path, "PATCH", func)

        return decorator

    def head(self, path: str):
        def decorator(func):
            return self._route(path, "HEAD", func)

        return decorator

    def options(self, path: str):
        def decorator(func):
            return self._route(path, "OPTIONS", func)

        return decorator

    def trace(self, path: str):
        def decorator(func):
            return self._route(path, "TRACE", func)

        return decorator

    def connect(self, path: str):
        def decorator(func):
            return self._route(path, "CONNECT", func)

        return decorator

    def static(self, path: str):
        return self._route(path, "GET", None, is_static=True)

    def _get_route(self, path: str) -> Route | None:
        if "." in path.split("/")[-1]:
            for route in self.static_routes:
                if path.startswith(route.path):
                    return route
            return None
        for route in self.routes:
            if route.path == path:
                return route
        return None

    def __contains__(self, path: str) -> bool:
        return any([route.path == path for route in self.routes])
