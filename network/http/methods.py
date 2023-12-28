from httpRouter import Request, Response, HttpStatusCode, HTTPServer
from configs import app, FILE_SERVER
from httpRouter import get_content_type


@app.get("/calculate-next")
def _(req: Request) -> Response:
    if "num" not in req.params or not req.params["num"].isnumeric():
        return Response(code=HttpStatusCode.BAD_REQUEST)
    return Response(data=bytes(str(int(req.params["num"]) + 1), "utf-8"))


@app.get("/calculate-area")
def _(req: Request) -> Response:
    if (
        "width" not in req.params
        or "height" not in req.params
        or not req.params["width"].isnumeric()
        or not req.params["height"].isnumeric()
    ):
        return Response(code=HttpStatusCode.BAD_REQUEST)
    return Response(
        data=bytes(
            str(int(req.params["width"]) * int(req.params["height"]) / 2), "utf-8"
        )
    )


@app.post("/upload")
def _(req: Request) -> Response:
    if "file-name" not in req.params:
        return Response(code=HttpStatusCode.BAD_REQUEST)
    with open(f"{FILE_SERVER}/uploads/{req.params['file-name']}", "wb") as f:
        data = req.raw_data
        while True:
            f.write(data)
            try:
                data = req.sock.recv(1024)
            except:
                break
    return Response(code=HttpStatusCode.OK)


@app.get("/image")
def _(req: Request) -> Response:
    if "image-name" not in req.params:
        return Response(code=HttpStatusCode.BAD_REQUEST)
    with open(f"{FILE_SERVER}/uploads/{req.params['image-name']}", "rb") as f:
        return Response(
            data=f.read(),
            headers={"Content-Type": get_content_type(req.params["image-name"])},
        )
