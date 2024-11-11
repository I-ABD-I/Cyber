def main():
    with open(r"\\.\pipe\chat", "r+b") as pipe:
        msg = input()
        pipe.write(msg.encode())
        res = pipe.read()
        print(res)


if __name__ == "__main__":
    main()
