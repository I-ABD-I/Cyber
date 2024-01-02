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

WEBROOT_PATH = "./"

HTTP_STATUS_OK = "HTTP/1.1 200 OK\r\n"
HTTP_STATUS_NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"
HTTP_STATUS_REDIRECT = "HTTP/1.1 302 Found\r\n"
HTTP_STATUS_INTERNAL_SERVER_ERROR = "HTTP/1.1 500 Internal Server Error\r\n"

HTTP_HTML_HEADER = "Content-Type: text/html; charset=utf-8\r\n"
HTTP_JPG_HEADER = "Content-Type: image/jpg\r\n"
HTTP_JS_HEADER = "Content-Type: text/javascript; charset=utf-8\r\n"
HTTP_CSS_HEADER = "Content-Type: text/css; charset=utf-8\r\n"
HTTP_PLAIN_HEADER = "Content-Type: text/plain; charset=utf-8\r\n"


def GET_calculate_next(params: dict[str, str]) -> bytes:
    if "num" in params and params["num"].isnumeric():
        return str(int(params["num"]) + 1).encode()
    return b"Error check params"


def GET_calculate_area(params: dict[str, str]) -> bytes:
    if (
        "width" in params
        and "height" in params
        and params["width"].isnumeric()
        and params["height"].isnumeric()
    ):
        return str(int(params["width"]) * int(params["height"]) / 2).encode()
    return b"Error check params"

def GET_image(params: dict[str, str]) -> bytes:
    if "image-name" in params:
        with open(f"{WEBROOT_PATH}uploads/{params["image-name"]}", "rb") as f:
            return f.read()
    return b"Error check params"

GET_METHODS = {
    "/calculate-next": GET_calculate_next,
    "/calculate-area": GET_calculate_area,
    "/image": GET_image,
}


def POST_upload(params: dict[str, str], data: bytes, client_socket) -> bool:
    try:
        with open(f"{WEBROOT_PATH}uploads/{params["file-name"]}", "wb") as f:
            while data:
                f.write(data)
                try:
                    data = client_socket.recv(1024)
                except socket.timeout:
                    break
        return True
    except:
        return False


POST_METHODS = {"/upload": POST_upload}


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
        data = GET_METHODS[url](params)
        if "image-name" in params:
            url = f"/uploads/{params["image-name"]}"
        filelen = len(data)
    else:
        if os.path.isfile(f"{WEBROOT_PATH}{url}"):
            data = get_file_data(f"{WEBROOT_PATH}{url}")
            filelen = len(data)
        else:
            status_code = HTTP_STATUS_NOT_FOUND
            data = b""
            filelen = 0


    location_header = ""
    if url in REDIRECTION_DICTIONARY:
        status_code = HTTP_STATUS_REDIRECT
        location_header = f"Location: {REDIRECTION_DICTIONARY[url]}\r\n"

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

    http_header = f"{status_code}{header}{location_header}Content-Length: {filelen}\r\n\r\n".encode()

    http_response = http_header + data
    client_socket.send(http_response)


def handle_post(client_socket: socket.socket, resource: str, data: bytes):
    status_code = HTTP_STATUS_OK
    url = resource if resource != "/" else DEFAULT_URL

    url, params = url.split("?") if "?" in url else (url, "")

    if url in POST_METHODS:
        params = dict([param.split("=") for param in params.split("&")])
        isSuccess = POST_METHODS[url](params, data, client_socket)
        if not isSuccess:
            status_code = HTTP_STATUS_INTERNAL_SERVER_ERROR
    else:
        status_code = HTTP_STATUS_NOT_FOUND

    http_header = f"{status_code}Content-Length: 0\r\n\r\n".encode()
    client_socket.send(http_header)


def validate_http_request(request: bytes) -> tuple[bool, str, str]:
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    httpreg = re.compile(r"^(.*)\s(.*)\sHTTP/1.1")
    request = request.split(b"\r\n")[0]
    m = httpreg.match(request.decode())
    return (
        (m.group(1) in {"GET", "POST"}, m.group(2), m.group(1))
        if m
        else (False, "", "")
    )


def handle_client(client_socket: socket.socket):
    """Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests"""
    print("Client connected")

    while True:
        try:
            client_request = client_socket.recv(1024)
            valid_http, resource, method = validate_http_request(client_request)
            if not client_request:
                break
            data = client_request.split(b"\r\n\r\n")[1]
            if valid_http:
                print("Got a valid HTTP request")
                if method == "GET":
                    handle_client_request(resource, client_socket)
                elif method == "POST":
                    handle_post(client_socket, resource, data)
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
