from enum import Enum
from pathlib import Path
import shlex
import sys
import subprocess
import webbrowser
from setup_game import CRACK_TYPES, is_complete, one_time_setup
from config_loader import BASE_PATH, GAMEVAULT_EXEC_CONFIG, Config, get_config_value, set_config_values, script_version
from validate import validate_paths
from lang import lang
from util import clear_screen, get_exe_path, sleep
from version_changer import change_version
from gamevault_exec_handler import GVExecConfig
from symlink import move_source_and_link_dir, parse_move_link_input
from logger import console
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import color_print
from send_to_friend import send_to_friend

# ----------------------------
# Functions
# ----------------------------

# 1. Start game
def start_game(reset: bool = True):
    gv_config = GVExecConfig(GAMEVAULT_EXEC_CONFIG)
    console.print(lang["start.starting_game"])
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "False").lower() == "true"
    is_original = get_config_value(Config.Default.str(), Config.Default.GameVersion, "Pirated").lower() == "original"
    steam_appid = get_config_value(Config.Default.str(), Config.Default.SteamAppID, "-1")
    exe_path = Path(get_config_value(Config.Default.str(), Config.Default.Executable))
    launch_parameter = get_config_value(Config.Default.str(), Config.Default.LaunchParameter, "")
    if is_original:
        if steam_appid != "-1": # if no steam id
            webbrowser.open(f"steam://run/{steam_appid}")
            sleep(1)
            sys.exit(0)
        # else, fallback to other methods

    if not no_gamevault_mode:
        # Update executable of gamevault-exec temporarily
        gv_config.set_executable(str(exe_path.resolve()))
        curr_param = gv_config.get_launch_parameter()
        no_existing_param = not curr_param or curr_param == ""
        if no_existing_param:
            gv_config.set_launch_parameter(launch_parameter)
        set_config_values(Config.Default.str(), Config.Default.DontAskAgain, "False")
            
        # GV game's launch exe is set to the actual game's .exe, just open browser then reset
        gamevault_game_id = get_config_value(Config.Default.str(), Config.Default.GameVaultGameID, default="-1")
        if gamevault_game_id == "-1":
            raise ValueError("validate.errors.gamevault_game_id")
        webbrowser.open(f"gamevault://start?gameid={gamevault_game_id}")
        sleep(1)

        # no need to reset if it was already default
        if reset:
            gv_config.set_executable(get_exe_path()) # revert to this python.exe
            gv_config.set_launch_parameter("")
        sys.exit(0)
    else:
        # run exe with param
        if exe_path.exists() and exe_path.is_file():
            split_params = shlex.split(launch_parameter, posix=False)
            exec_command = [str(exe_path)] + split_params
            subprocess.Popen(exec_command, cwd=exe_path.parent)
            sleep(1)
            sys.exit(0)
        else:
            console.print(lang["start.exec_path_not_found"])
            sleep(2)


# 2. Start game and don't ask again
def start_game_no_prompt():
    console.print(lang["start.updated_exec_file"])
    sleep(3)
    # Update executable of gamevault-exec
    start_game(reset = False)

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
    ChangeVersion = 3,
    SendToFriend = 4

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
        choices.append(Choice(value=MenuChoices.SendToFriend,   name="Send to Friend"))
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

def reset_default_exec():
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "False").lower == "True"
    if not no_gamevault_mode:
        return

    # Update executable of gamevault-exec temporarily
    gv_config = GVExecConfig(GAMEVAULT_EXEC_CONFIG)
    gv_config.set_executable(get_exe_path())
    gv_config.set_launch_parameter("")
    set_config_values(Config.Default.str(), Config.Default.DontAskAgain, "False")

# ----------------------------
# Main prompt loop
# ----------------------------
def main():
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
        case MenuChoices.SendToFriend:
            send_to_friend()
        case _:
            sys.exit(0)

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    try:
        validate_paths() # must always take precedence
        reset_default_exec()
        setup_links()
        while True:
            main()
            clear_screen()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")