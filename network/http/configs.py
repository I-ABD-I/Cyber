from httpRouter import HTTPServer

FILE_SERVER = "./webroot"

app = HTTPServer(file_server=FILE_SERVER)
