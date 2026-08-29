import os
from pathlib import Path
import shutil
import sys
import time
from typing import Tuple

from InquirerPy.utils import color_print
from logger import console
from lang import lang

def get_exe_path() -> Path:
    return Path(sys.executable).resolve()

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

# scrapes for the original steam_api.dll
def find_file(filename: str, search_path: str, exclude_dir: str) -> Path:
    for path in Path(search_path).rglob(filename):
        if exclude_dir not in path.parts:
            return path
    return None

def copy_files_from_reference(search_path: Path, reference_dir: Path, destination: Path) -> Tuple[set[Path], set[Path]]:
    return find_files_from_reference(search_path=search_path, reference_dir=reference_dir, destination=destination)

def find_files_from_reference(search_path: Path, reference_dir: Path, destination: Path | None) -> Tuple[set[Path], set[Path]]:
    found_files = set()
    found_ref_files = set()
    # 3. Scan reference dirs files to look for it in BASE_PATH
    for ref_file in reference_dir.rglob("*"):
        if not ref_file.is_file():
            continue
        
        # Get relative file to look for in 
        relative = ref_file.relative_to(reference_dir) # ex ref_dir/dir1/file becomes dir1/file
        found_ref_files.add(ref_file)
        
        source = search_path / relative # concatenate, ex. becomes search_path/dir1/file
        if not source.exists() or not source.is_file():
            continue
        
        if destination:
            actual_destination = destination / relative
            actual_destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, actual_destination)

        found_files.add(ref_file)

    # 4. find files
    return found_files, found_ref_files

def render_text(config, variables=None):
    variables = variables or {}

    formatted_text = []

    for item in config["title"]:
        text = item["text"]

        for key, value in variables.items():
            text = text.replace(f"{{{{{key}}}}}", str(value))

        style = item.get("style", "")
        class_name = f"class:{style}" if style else ""

        formatted_text.append((class_name, text))

    color_print(
        formatted_text=formatted_text,
        style=config["styles"],
    )