from enum import Enum
from pathlib import Path
import sys
import subprocess
from setup_game import CRACK_TYPES, is_complete, one_time_setup
from config_loader import BASE_PATH, GAMEVAULT_EXEC_CONFIG, Config, get_config_value, set_config_values, script_version, validate_paths
from util import clear_screen, get_exe_path, sleep
from version_changer import change_version
from gamevault_exec_handler import set_executable
from logger import console
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print

# ----------------------------
# Functions
# ----------------------------

# 1. Start game
def start_game():
    # reset Don't Ask Again
    dont_ask_again = get_config_value(Config.Default.str(), Config.Default.DontAskAgain, "False").lower() == "true"
    if (dont_ask_again):
        set_config_values(Config.Default.str(), Config.Default.DontAskAgain, "False")
        set_executable(get_exe_path()) # revert to this python.exe
    # run exe
    exe_path = get_config_value(Config.Default.str(), Config.Default.Executable)
    exe_path = Path(exe_path)

    if exe_path.exists() and exe_path.is_file():
        console.print(f"Starting game...")
        subprocess.Popen(exe_path)
        sys.exit(0)
    else:
        console.print("[red]Executable path not found in external config.")
        sleep(2)

# 2. Start game and don't ask again
def start_game_no_prompt():
    # Update executable of gamevault-exec
    set_executable(str(BASE_PATH / get_config_value(Config.Default.str(), Config.Default.Executable)))
    
    console.print(f"Updated gamevault-exec file to skip prompt next time.")
    sleep(2)
    start_game()

# 4. Change version (delete files in __folder1, merge __folder2 into base)
def prompt_change_version():
    choice = inquirer.select(
        message=get_change_version_choice_str()+":",
        choices=[
            "Original",
            "Pirated",
            Choice(value=None, name="Back")
        ],
        default="Original",

    ).execute()

    if choice is None:
        clear_screen()
        return
    #clear_screen()
    change_version(version=choice)

class MenuChoices(Enum):
    Start = 0,
    StartAlways = 1,
    Setup = 2,
    ChangeVersion = 3

def get_setup_choice_str(setup_type: str, setup_done: bool):
    is_error = False
    # Build option 3 string
    match CRACK_TYPES[setup_type]:
        case CRACK_TYPES.OnlineFix:
            choice_string = f"One-time global setup for '{setup_type}'"
        case CRACK_TYPES.Goldberg:
            choice_string = f"One-time global setup for '{setup_type}'"
        case CRACK_TYPES.RUNE:
            choice_string = f"Per-Game Setup for '{setup_type}'"
        case CRACK_TYPES.Other:
            choice_string = f"Per-Game Setup"
        case _:
            choice_string = "Option error, Contact GameVault Admin!"
            is_error = True
    if setup_done and not is_error:
        choice_string += " (complete)"
    
    return choice_string
def get_change_version_choice_str():
    choice_string = "Change version"
    current_version = get_config_value(Config.Default.str(), Config.Default.GameVersion, "")
    if current_version:
        choice_string += f". Current: {current_version}"
    return choice_string

def setup_choices():
    setup_type = get_config_value(Config.Crack.str(), Config.Crack.Type, "CONTACT GAMEVAULT ADMIN")
    setup_done = is_complete()
    has_setup = get_config_value(Config.Crack.str(), Config.Crack.NoSetup, "False").lower() == "false"
    has_original = get_config_value(Config.Default.str(), Config.Default.NoOriginal, "False").lower() == "false"

    choices: list = []
    if setup_done:
        choices.append(Choice(value=MenuChoices.Start,         name="Start game"))
        choices.append(Choice(value=MenuChoices.StartAlways,   name="Start game and don't ask again"))
        if has_setup:
            choices.append(Choice(value=MenuChoices.Setup,     name=get_setup_choice_str(setup_type, setup_done)))
        if has_original:
            choices.append(Choice(value=MenuChoices.ChangeVersion, name=get_change_version_choice_str()))
    else:
        choices.append(Choice(value=MenuChoices.Setup,     name=get_setup_choice_str(setup_type, setup_done)))

    choices.append(Choice(value=None, name="Exit"))

    return choices

# ----------------------------
# Main prompt loop
# ----------------------------
def main():
    color_print(formatted_text=[
                    ("class:gg", "Game"),
                    ("", "Vault"),
                    ("class:yy", " Utility"),
                    ("", " - "),
                    ("class:vv", script_version)
                ],
                style={
                    "": "bold underline",
                    "yy": "cyan",
                    "gg": "#4f46af",
                    "vv": "yellow"
                })

    choices = setup_choices()
    choice: MenuChoices | None = inquirer.select(
        message="Select an option:",
        choices=choices,
        instruction="Use Arrow Keys",
        default="Original",
    ).execute()
    
    match choice:
        case MenuChoices.Start:
            start_game()
        case MenuChoices.StartAlways:
            start_game_no_prompt()
        case MenuChoices.Setup:
            one_time_setup()
        case MenuChoices.ChangeVersion:
            prompt_change_version()
        case _:
            sys.exit(0)

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    try:
        while True:
            validate_paths()
            main()
            clear_screen()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")