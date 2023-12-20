import sys

FILE1 = sys.argv[1]
FILE2 = sys.argv[2]

if __name__ == "__main__":
    with open(FILE1, "r") as read:
        with open(FILE2, "w") as write:
            write.write(read.read())
