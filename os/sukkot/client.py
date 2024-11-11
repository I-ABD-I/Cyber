"""
Written By : Aylon
Date       : 16 / 10 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

import queue
import re
import socket
import subprocess
import sys
import threading
from math import e

# region ------------------- Imports -------------------
from os import error
from typing import Iterable

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# endregion


# region ------------------- Engine -------------------
class Engine(threading.Thread):
    def __init__(
        self, msgq: queue.Queue[str], resq: queue.Queue[Iterable[str] | None]
    ) -> None:
        threading.Thread.__init__(self)
        self.daemon = True
        self.msgq = msgq
        self.resq = resq
        self.socket = socket.socket()

        self.socket.connect(("127.0.0.1", 8080))  # handle Error on main

    def run(self) -> None:
        running = True
        while running:
            msg = self.msgq.get()
            try:
                self.socket.send(msg.encode())
                response = self.socket.recv(1024).decode()
            except socket.error as e:
                print(e)

            if response == "N/A":
                self.resq.put(None)
                continue

            self.handle_response(response)

    def handle_response(self, response: str):
        try:
            _, cmd, regex = response.split("@")
            process = subprocess.run(cmd.split(), capture_output=True)
            if regex:
                self.resq.put(
                    line
                    for line in process.stdout.decode().splitlines()
                    if re.search(regex, line)
                )
            else:
                self.resq.put((process.stdout.decode(),))
        except Exception as e:
            print(e)


# endregion


# region ------------------- GUI -------------------
class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.msgq = queue.Queue()
        self.resq = queue.Queue()
        try:
            self.engine = Engine(self.msgq, self.resq)
        except socket.error:
            print("Failed to connect to server... quitting")
            exit(-1)
        self.engine.start()

        layout = QVBoxLayout()
        self.lbl = QLabel()
        sa = QScrollArea()
        sa.setFixedSize(1000, 500)
        sa.setWidget(self.lbl)
        sa.setWidgetResizable(True)
        layout.addWidget(sa)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.on_msg)
        layout.addWidget(self.input)

        self.setLayout(layout)
        self.show()

    def on_msg(self):
        self.msgq.put(self.input.text())
        self.input.setText(None)
        to_display = self.resq.get()
        self.lbl.setText(
            "\n".join(to_display) if to_display else "Error Unknown Command!"
        )


# endregion


# region ------------------- Main -------------------
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
# endregion
