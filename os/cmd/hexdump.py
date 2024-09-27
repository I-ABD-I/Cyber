"""
Written By : Aylon
Date       : 25 / 09 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

import sys


def main():
    if len(sys.argv) == 1:
        print("Missing File")
        exit(-1)
    path = sys.argv[1]
    try:
        with open(path, "rb") as file:
            while bytes := file.read(8):
                print(f"{" ".join(f"{byte:02x}" for byte in bytes)}")
    except FileNotFoundError as e:
        print(e)
if __name__ == "__main__":
    main()
