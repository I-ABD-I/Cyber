"""
Written By : Aylon
Date       : 25 / 09 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Imports -------------------
import re
import sys
from typing import TextIO

# endregion


def match(regex, stream: TextIO):
    try:
        for line in stream:
            if re.search(regex, line):
                print(line)
    except re.error:
        print("Invalid Regex")


def main():
    if len(sys.argv) == 3:
        try:
            match(sys.argv[1], open(sys.argv[2], "r"))
        except FileNotFoundError as e:
            print(e)
    elif len(sys.argv) == 2:
        match(sys.argv[1], sys.stdin)
    else:
        print("Invalid Params")


if __name__ == "__main__":
    main()
