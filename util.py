import os
from pathlib import Path
import sys
import time
import uuid
from logger import console
from lang import lang

def get_exe_path() -> Path:
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app 
        # path into variable _MEIPASS'.
        return Path(sys._MEIPASS).resolve()
    else:
        return Path(__file__).resolve()

    # for --onefile
    # if getattr(sys, 'frozen', False):
    #     return Path(sys.executable).resolve()
    # return Path(__file__).resolve()

def prompt_yes_no(message: str, default: bool | None = None) -> bool:
    """
    Ask a yes/no question and return True for yes, False for no.

    default:
        True  -> [Y/n]
        False -> [y/N]
        None  -> [y/n] (no default)
    """
    if default is True:
        suffix = " [Y/n]: "
    elif default is False:
        suffix = " [y/N]: "
    else:
        suffix = " [y/n]: "

    while True:
        choice = input(message + suffix).strip().lower()

        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False

        if choice == "" and default is not None:
            return default

        console.print(lang["messages.invalid_yes_no"])

def pause(clear: bool = False):
    console.print()
    input("Press Enter to continue...")
    if clear:
        clear_screen()
    else:
        console.print()
    clear_input_buffer()

def clear_screen():
    """
    Clears the terminal screen for Windows, macOS, and Linux.
    """
    try:
        # Detect the operating system
        
        if os.name == "nt":
            os.system('cls')  # Windows clear command
        else:
            os.system('clear')  # macOS/Linux clear command
    except Exception as e:
        console.print(lang["errors.clear_screen_error"](error=str(e)))

def clear_input_buffer():
    try:
        # Windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        # Unix
        import sys
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    
def sleep(seconds: float):
    time.sleep(seconds)
    clear_input_buffer()