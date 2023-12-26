# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import re
import os

# TO DO: set constants
IP = "0.0.0.0"
PORT = 80
SOCKET_TIMEOUT = 0.1
FIXED_RESPONSE = "ERROR 404: Page not found"
DEFAULT_URL = "/index.html"
REDIRECTION_DICTIONARY = {}

HTTP_STATUS_OK = "HTTP/1.1 200 OK\r\n"
HTTP_STATUS_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
HTTP_STATUS_REDIRECT = "HTTP/1.1 302 Found\r\n"

HTTP_HTML_HEADER = "Content-Type: text/html; charset=utf-8\r\n"
HTTP_JPG_HEADER = "Content-Type: image/jpg\r\n"
HTTP_JS_HEADER = "Content-Type: text/javascript; charset=utf-8\r\n"
HTTP_CSS_HEADER = "Content-Type: text/css; charset=utf-8\r\n"
HTTP_PLAIN_HEADER = "Content-Type: text/plain; charset=utf-8\r\n"


def GET_calculate_next(params: dict[str, str]) -> str:
    if "num" in params and params["num"].isnumeric():
        return str(int(params["num"]) + 1)
    return "Error check params"


def GET_calculate_area(params: dict[str, str]) -> str:
    if (
        "width" in params
        and "height" in params
        and params["width"].isnumeric()
        and params["height"].isnumeric()
    ):
        return str(int(params["width"]) * int(params["height"]) / 2)
    return "Error check params"


GET_METHODS = {
    "/calculate-next": GET_calculate_next,
    "/calculate-area": GET_calculate_area,
}


def get_file_data(filename) -> bytes:
    """Get data from file"""
    with open(filename, "rb") as f:
        data = f.read()
    return data


def handle_client_request(resource: str, client_socket: socket.socket):
    """Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response

    status_code = HTTP_STATUS_OK
    url = resource if resource != "/" else DEFAULT_URL

    url, params = url.split("?") if "?" in url else (url, "")

    if url in GET_METHODS:
        params = dict([param.split("=") for param in params.split("&")])
        data = GET_METHODS[url](params).encode()
        filelen = len(data)
    else:
        if os.path.isfile(f"./{url}"):
            data = get_file_data(f"./{url}")
            filelen = len(data)
        else:
            status_code = HTTP_STATUS_NOT_FOUND
            data = b""
            filelen = 0

    if url in REDIRECTION_DICTIONARY:
        status_code = HTTP_STATUS_REDIRECT

    filetypereg = re.compile(r"/(.*)\.(.*)")
    m = filetypereg.match(url)

    filetype = m.group(2) if m else ""

    header_map = {
        "html": HTTP_HTML_HEADER,
        "jpg": HTTP_JPG_HEADER,
        "js": HTTP_JS_HEADER,
        "css": HTTP_CSS_HEADER,
    }
    header = header_map.get(filetype, HTTP_PLAIN_HEADER)

    http_header = f"{status_code}{header}Content-Length: {filelen}\r\n\r\n".encode()

    http_response = http_header + data
    client_socket.send(http_response)


def validate_http_request(request) -> tuple[bool, str]:
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    httpreg = re.compile(r"^GET\s(.*)\sHTTP/1.1")
    m = httpreg.match(request)
    return (True, m.group(1)) if m else (False, "")


def handle_client(client_socket: socket.socket):
    """Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests"""
    print("Client connected")

    while True:
        try:
            client_request = client_socket.recv(1024).decode()
            valid_http, resource = validate_http_request(client_request)
            if valid_http:
                print("Got a valid HTTP request")
                handle_client_request(resource, client_socket)
                break
            else:
                print("Error: Not a valid HTTP request")
                break
        except socket.timeout:
            print("Timed out")
            break

    print("Closing connection")
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, _ = server_socket.accept()
        print("New connection received")
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
