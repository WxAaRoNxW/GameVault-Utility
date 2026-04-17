import ctypes
from enum import Enum
from pathlib import Path
import sys
import subprocess
from setup_game import CRACK_TYPES, is_complete, one_time_setup
from config_loader import BASE_PATH, DEBUG, GAMEVAULT_EXEC_CONFIG, Config, get_config_value, set_config_values, script_version
from validate import validate_paths
from lang import lang
from util import clear_screen, get_exe_path, sleep
from version_changer import change_version
from gamevault_exec_handler import set_executable
from symlink import move_source_and_link_dir, parse_move_link_input
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
        console.print(lang["start.starting_game"])
        
        subprocess.Popen(exe_path)
        sys.exit(0)
    else:
        console.print(lang["start.exec_path_not_found"])
        sleep(2)

# 2. Start game and don't ask again
def start_game_no_prompt():
    # Update executable of gamevault-exec
    set_executable(str(BASE_PATH / get_config_value(Config.Default.str(), Config.Default.Executable)))
    
    console.print(lang["start.updated_exec_file"])
    sleep(3)
    start_game()

# 4. Change version (delete files in __folder1, merge __folder2 into base)
def prompt_change_version():
    choice = inquirer.select(
        message=get_change_version_choice_str()+":",
        choices=[
            lang["change_version.original"],
            lang["change_version.modified"],
            Choice(value=None, name=lang["change_version.back_option"])
        ],
        default=lang["change_version.original"],

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
            choice_string = lang["main_menu.one_time_for_x"](setup_type=setup_type)
        case CRACK_TYPES.Goldberg:
            choice_string = lang["main_menu.one_time_for_x"](setup_type=setup_type)
        case CRACK_TYPES.RUNE:
            choice_string = lang["main_menu.per_game_for_x"](setup_type=setup_type)
        case CRACK_TYPES.Other:
            choice_string = lang["main_menu.per_game_default"]
        case CRACK_TYPES.Goldberg_Old:
            choice_string = lang["main_menu.one_time_for_x"](setup_type=setup_type)
        case _:
            choice_string = lang["main_menu.option_error"]
            is_error = True
    if setup_done and not is_error:
        choice_string += " (complete)"

    return choice_string
def get_change_version_choice_str():
    choice_string = lang["change_version.message"]
    current_version = get_config_value(Config.Default.str(), Config.Default.GameVersion, "")
    if current_version:
        choice_string += ". " + lang["change_version.current_version"](version=current_version)
    return choice_string

def setup_choices():
    setup_type = get_config_value(Config.Crack.str(), Config.Crack.Type, "CONTACT GAMEVAULT ADMIN")
    setup_done = is_complete()
    has_setup = get_config_value(Config.Crack.str(), Config.Crack.NoSetup, "False").lower() == "false"
    has_original = get_config_value(Config.Default.str(), Config.Default.NoOriginal, "False").lower() == "false"
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "True").lower() == "true"
    choices: list = []
    if setup_done:
        if not no_gamevault_mode: choices.append(Choice(value=MenuChoices.StartAlways,   name=lang["main_menu.start_always"]))
        choices.append(Choice(value=MenuChoices.Start,         name=lang["main_menu.start"]))
        if has_setup:
            choices.append(Choice(value=MenuChoices.Setup,     name=get_setup_choice_str(setup_type, setup_done)))
        if has_original:
            choices.append(Choice(value=MenuChoices.ChangeVersion, name=get_change_version_choice_str()))
    else:
        choices.append(Choice(value=MenuChoices.Setup,     name=get_setup_choice_str(setup_type, setup_done)))

    choices.append(Choice(value=None, name=lang["main_menu.exit"]))

    return choices

def setup_links():
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "True").lower() == "true"
    if no_gamevault_mode:
        return # no gamevault mode is only ever used for instances with original version, so there's no need to symlink files that deletes on gamevault game update.
     
    setup_link_done = get_config_value(Config.Setup.str(), Config.Setup.PathMoveLinkingComplete, "False").lower() == "true"

    if setup_link_done: return

    pathlink_string = get_config_value(Config.Setup.str(), Config.Setup.PathMoveLinking, '')
    pathlink_config_empty = pathlink_string.strip() == ''
    if pathlink_config_empty:
        set_config_values(Config.Setup.str(), Config.Setup.PathMoveLinkingComplete, "True")
        return
    
    target_source_dict_list = parse_move_link_input(pathlink_string)
    move_source_and_link_dir(target_source_dict_list, exist_ok=True)

    set_config_values(Config.Setup.str(), Config.Setup.PathMoveLinkingComplete, "True")
# ----------------------------
# Main prompt loop
# ----------------------------
def main():
    setup_links()
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "True").lower() == "true"
    color_print(formatted_text=[
                    ("class:gg", "Game"),
                    ("", "Manager" if no_gamevault_mode else "Vault"),
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
        message=lang["main_menu.prompt_option.message"],
        choices=choices,
        instruction=lang["main_menu.prompt_option.instruction"],
        default=lang["change_version.original"],
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
    if not DEBUG:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print(lang["messages.requesting_admin"])
            params = f'"{sys.argv[0]}" {" ".join(sys.argv[1:])}'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)

    try:
        while True:
            validate_paths()
            main()
            clear_screen()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")