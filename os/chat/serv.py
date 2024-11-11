import multiprocessing
from multiprocessing.connection import PipeConnection


def client(conn: PipeConnection):
    if conn.recv():
        conn.send(input())

    while True:
        print(conn.recv())
        conn.send(input())


def main():
    lst = []
    p1, child = multiprocessing.Pipe()

    proc = multiprocessing.Process(target=client, args=(child,))
    proc.start()
    lst += [proc]
    p2, child = multiprocessing.Pipe()
    proc = multiprocessing.Process(target=client, args=(child,))
    proc.start()
    lst += [proc]

    while True:
        p1.send(True)
        p2.send(False)

        msg = p1.recv()
        print(msg)
        p2.send(msg)

        msg = p2.recv()
        print(msg)
        p1.send(msg)

    for p in lst:
        p.join()


if __name__ == "__main__":
    main()
