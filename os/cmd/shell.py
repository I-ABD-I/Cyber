"""
Written By : Aylon
Date       : 25 / 09 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Import -------------------
import getpass
import itertools
import os
import socket
import subprocess
import sys
from typing import IO

import colorama

# endregion


# region ------------------- Exceptions -------------------
class UnknownCommand(Exception):
    def __init__(self, cmd, *args: object) -> None:
        super().__init__(*args)
        self.cmd = cmd


# endregion


# region ------------------- Functions -------------------
def launch(
    cmd: str, args: list[str], stdin: IO[bytes] | None = None
) -> IO[bytes] | None:
    match cmd:
        case "cd":
            os.chdir(args[0])
        case "set":
            os.environ[args[0]] = args[1]
        case "exit":
            exit(0)
        case _:
            if os.path.isfile(
                path := os.path.join(os.environ["SCRIPTS_FOLDER"], f"{cmd}.py")
            ):
                return launch("python", [path] + args, stdin)

            for i in itertools.chain(os.environ["PATH"].split(os.pathsep)):
                if os.path.isfile(os.path.join(i, f"{cmd}.exe")):
                    return subprocess.Popen(
                        [cmd] + args, stdout=subprocess.PIPE, stdin=stdin
                    ).stdout
    raise UnknownCommand(cmd)


def process_cmd(cmd: str):
    if ">" in cmd:
        cmd, file = cmd.split(">")
        stream = process_cmd(cmd)
        if stream:
            with open(file, "wb") as f:
                f.write(stream.read())
        return

    cmds = cmd.split("|")
    c, *args = cmds[0].strip().split(" ")
    prev = launch(c, args)
    for c in cmds[0:]:
        c, *args = c.strip().split(" ")
        prev = launch(c, args, prev)

    return prev


# endregion


# region ------------------- Main -------------------
def main():
    colorama.init()
    os.environ["SCRIPTS_FOLDER"] = sys.argv[1] if len(sys.argv) == 2 else "./"
    running = True
    while running:
        try:
            cmd = input(
                f"{colorama.Fore.GREEN}{getpass.getuser()}@{socket.gethostname()}:{colorama.Fore.BLUE}{os.getcwd()}{colorama.Style.RESET_ALL}$ "
            )
            try:
                if output := process_cmd(cmd):
                    print(output.read().decode())
            except UnknownCommand as e:
                print(f"Unknown Command {e.cmd}")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
# endregion
