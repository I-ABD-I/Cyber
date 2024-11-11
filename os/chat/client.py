from sys import stdin, stdout


def main():
    msg = stdin.read()
    print(msg)
    res = input()
    stdout.write(res)


if __name__ == "__main__":
    main()
