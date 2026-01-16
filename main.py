from enum import Enum
from pathlib import Path
import sys
import subprocess
from setup_game import CRACK_TYPES, is_complete, one_time_setup
from config_loader import BASE_PATH, GAMEVAULT_EXEC_CONFIG, Config, get_config_value, set_config_values
from util import clear_screen, get_exe_path, sleep
from version_changer import change_version
from gamevault_exec_handler import set_executable
from logger import console
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

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
        console.print(f"Starting game: {exe_path}")
        subprocess.run(exe_path)
        sys.exit("Exiting...")
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

def get_setup_choice_str():
    # Load suffix info from external config
    setup_type = get_config_value(Config.Crack.str(), Config.Crack.Type, "CONTACT GAMEVAULT ADMIN")
    setup_done = is_complete()
    # Build option 3 string
    match CRACK_TYPES[setup_type]:
        case CRACK_TYPES.OnlineFix:
            choice_string = f"One-time global setup for '{setup_type}'"
        case CRACK_TYPES.Goldberg:
            choice_string = f"One-time global setup for '{setup_type}'"
        case CRACK_TYPES.RUNE:
            choice_string = f"Per-Game Setup for '{setup_type}'"
        case _:
            choice_string = "Option error, Contact GameVault Admin!"
    if setup_done:
        choice_string += " (complete)"
    else:
        choice_string += " (DO THIS FIRST)"
    
    return choice_string
def get_change_version_choice_str():
    choice_string = "Change version"
    current_version = get_config_value(Config.Default.str(), Config.Default.GameVersion, "")
    if current_version:
        choice_string += f". Current: {current_version}"
    return choice_string

# ----------------------------
# Main prompt loop
# ----------------------------
def main():
    choice: MenuChoices | None = inquirer.select(
        message="Select an option:",
        choices=[
            Choice(value=MenuChoices.Start,         name="Start game"),
            Choice(value=MenuChoices.StartAlways,   name="Start game and don't ask again"),
            Choice(value=MenuChoices.Setup,         name=get_setup_choice_str()),
            Choice(value=MenuChoices.ChangeVersion, name=get_change_version_choice_str()),
            Choice(value=None, name="Exit")
        ],
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
            sys.exit("Exiting...")

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    while True:
        try:
            main()
            clear_screen()
        except Exception as e:
            import traceback
            traceback.print_exc()
            input("\nPress Enter to exit...")