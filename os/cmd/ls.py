"""
Written By : Aylon
Date       : 25 / 09 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Imports -------------------
import os
import stat
import sys
import time

# endregion


# region ------------------- Main -------------------
def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "./"
    for entry in os.scandir(folder):
        info = entry.stat()
        perms = stat.filemode(info.st_mode)
        _time = time.strftime("%d/%m/%Y %H:%M", time.localtime(info.st_mtime))
        size = info.st_size
        print(f"{perms}  {_time:<10} {size:<8} {entry.name}")


if __name__ == "__main__":
    main()
# endregion
