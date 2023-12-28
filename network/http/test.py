from httpRouter import *
import methods
from configs import app


def main():
    app.static("/")
    app.start()


if __name__ == "__main__":
    main()
