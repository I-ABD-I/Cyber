"""
Written By : Aylon
Date       : 28 / 10 / 2024
Environment: VSCode
Python     : 3.12.1
OS         : Windows
"""

# region ------------------- Import -------------------
import ctypes
import ctypes.wintypes
import time

import win32api
import win32clipboard
import win32con
import win32gui
import win32ui

# endregion


# region ------------------- EX1 -------------------
def ex1():
    win32gui.MessageBox(
        None, "Aylon Ben Dvora", "Hi there", win32con.MB_YESNO | win32con.MB_HELP
    )

    win32api.MessageBox(
        None,
        "Aylon Ben Dvora",
        "Hi there :)",
        win32con.MB_YESNO | win32con.MB_HELP,
    )

    win32ui.MessageBox(
        "Aylon Ben Dvora",
        "Hi there :)",
        win32con.MB_YESNO | win32con.MB_HELP,
    )

    user32 = ctypes.WinDLL("User32.dll")
    user32.MessageBoxW(
        0,
        "Aylon Ben Dvora",
        "Hi there :)",
        win32con.MB_YESNO | win32con.MB_HELP,
    )


# endregion


# region ------------------- EX2 -------------------
def ex2():
    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HANDLE, ctypes.c_int)
    def cb(hwnd, n) -> bool:
        print(win32gui.GetWindowText(hwnd))
        return True

    user32 = ctypes.WinDLL("User32.dll")
    user32.EnumWindows(cb, 0)


# endregion


# region ------------------- EX3 -------------------
def ex3():
    running = True
    oldsn = win32clipboard.GetClipboardSequenceNumber()
    while running:
        win32clipboard.OpenClipboard()
        if (sn := win32clipboard.GetClipboardSequenceNumber()) != oldsn:
            oldsn = sn
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                print(
                    f"New Text Copied {win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)}"
                )
        win32clipboard.CloseClipboard()
        time.sleep(0.5)


# endregion
