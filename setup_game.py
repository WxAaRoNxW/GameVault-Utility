from enum import Enum
import os
from pathlib import Path
import time
import webbrowser
from config_loader import Config, get_config_value, set_config_values
from global_config import GlobalConfig, get_global_config_value, set_global_config_value
from util import clear_screen, clear_stdin, pause, prompt_yes_no, validate_steam_id
from logger import console

class CRACK_TYPES(Enum):
    OnlineFix = 0
    Goldberg = 1,
    RUNE = 2

def mark_done(setup_type: CRACK_TYPES):
    match setup_type:
        case CRACK_TYPES.OnlineFix:
            set_global_config_value(GlobalConfig.Setup.str(), GlobalConfig.Setup.OnlineFix, "True")
        case CRACK_TYPES.Goldberg:
            set_global_config_value(GlobalConfig.Setup.str(), GlobalConfig.Setup.Goldberg, "True")
        case CRACK_TYPES.RUNE:
            set_config_values(Config.Crack.str(), Config.Crack.SetupComplete, "True")
        case _:
            console.print("Can't identify crack type, contact GameVault admin.")
            pause(clear=True)

# 3. One-time global setup
def one_time_setup():
    # Get crack type
    setup_type = CRACK_TYPES[get_config_value(Config.Crack.str(), Config.Crack.Type, "N/A")]

    # Run crack type's method using switch case
    match setup_type:
        case CRACK_TYPES.OnlineFix:
            onlinefix_setup()
        case CRACK_TYPES.Goldberg:
            goldberg_setup()
        case CRACK_TYPES.RUNE:
            rune_setup()
        case _:
            console.print("Can't identify crack type, contact GameVault admin.")
            pause(clear=True)

def onlinefix_setup():
    if prompt_yes_no("Have you ever added Spacewar to your steam library in the past by installing and removing it?", False):
        clear_screen()
        console.print("Nothing to do")
        clear_screen()
        return
    
    clear_screen()
    console.print("Steam will pop-up to ask you to install Spacewar (to add to your library)")
    console.print("You can immediately cancel/remove as soon as you PRESS INSTALL")
    time.sleep(5)
    clear_stdin()
    webbrowser.open("steam://install/480")
    console.print("If the install menu doesn't show up, make sure you've logged-in or selected an account you'll use on steam.")
    console.print("Once done, setup is complete for EVERY OnlineFix games for THIS Steam account")
    pause(clear=True)
    mark_done(CRACK_TYPES.OnlineFix)

# Goldberg setup
def goldberg_setup():
    name_file = "account_name.txt"
    steam_id_file = "user_steam_id.txt"
    def modify_data(current_name, current_id):
        # Prompt user
        name_input = input(f"Enter your name to show in game (blank for default: {current_name}): ").strip()
        if not name_input: name_input = current_name
        clear_screen()

        webbrowser.open("https://steamid.xyz/")
        while True:
            console.print("Some games' save file are located in this Steam ID.")
            console.print("Best to stick to one Steam ID or else you'll have to manually migrate your save files when you change midway.")
            console.print("You can choose a fake or your own, doesn't matter.")
            console.print()
            console.print("A WEB PAGE OPENED for you to find your Steam ID")
            user_id_input = input(f"Enter your Steam64 ID (blank for default: {current_id}): ").strip()
            if not user_id_input: user_id_input = current_id

            clear_screen()
            if validate_steam_id(user_id_input): break
            
        # Write name.txt and id.txt
        (settings_folder / "account_name.txt").write_text(name_input, encoding="utf-8")
        (settings_folder / "user_steam_id.txt").write_text(user_id_input, encoding="utf-8")
        
        console.print(f"Setup complete for Goldberg in {settings_folder}")
        pause(clear=True)
        # Mark config complete
        mark_done(CRACK_TYPES.Goldberg)

    # Get user Roaming folder
    if os.name == "nt":
        roaming = Path(os.getenv("APPDATA"))
    else:
        roaming = Path.home() / ".config"
    
    settings_folder = roaming / "Goldberg SteamEmu Saves" / "settings"
    settings_folder.mkdir(parents=True, exist_ok=True)
    settings_name_path = settings_folder / name_file
    settings_id_path = settings_folder / steam_id_file
    account_name: str = "GY"
    id_content: str = "76561197960265728"
    exists = False
    # Check if files exists and Show existing data
    if settings_name_path.is_file():
        account_name = settings_name_path.read_text(encoding="utf-8").strip()
        console.print(f"Current username is, {account_name}")
        exists = True

    if settings_id_path.is_file():
        id_content = settings_id_path.read_text(encoding="utf-8").strip()
        console.print(f"Current steam id is, {id_content}")
        exists = True

    # Prompt setup to modify if exists
    if exists:
        proceed = prompt_yes_no("Proceed?...", True)
        if not proceed: return
        modify_data(account_name, id_content)
    # Else prompt setup
    else:
        modify_data(account_name, id_content)
    
    clear_screen()

# RUNE is a per game modification
def rune_setup():
    # check game version

    # find steam_emu.ini in _crack

    # edit username

    # edit id

    # modify cracked folder with config parser

    # copy to game if version choice is pirated

    # mark_done()
    console.print("Unimplemented")
    clear_screen()
    return

def is_complete() -> bool:
    setup_type = CRACK_TYPES[get_config_value(Config.Crack.str(), Config.Crack.Type, "")]
    setup_done = False
    match setup_type:
        case CRACK_TYPES.OnlineFix:
            # get global config value
            setup_done = get_global_config_value(GlobalConfig.Setup.str(), GlobalConfig.Setup.OnlineFix, "False").lower() == "true"
        case CRACK_TYPES.Goldberg:
            # Get user Roaming folder
            # if os.name == "nt":
            #     roaming = Path(os.getenv("APPDATA"))
            # else:
            #     roaming = Path.home() / ".config"
            
            # settings_folder = roaming / "Goldberg SteamEmu Saves" / "settings"
            # settings_folder.mkdir(parents=True, exist_ok=True)
            # name_file = "account_name.txt"
            # settings_name_path = settings_folder / name_file

            # # check if file exists
            # if not settings_name_path.is_file(): setup_done = False
            # # check if username is "Noob"
            # elif settings_name_path.read_text(encoding="utf-8").strip() == "Noob": setup_done = False
            # else: setup_done = True # already modified
            
            setup_done = get_global_config_value(GlobalConfig.Setup.str(), GlobalConfig.Setup.Goldberg, "False").lower() == "true"

        case CRACK_TYPES.RUNE:
            # just get config value in _crack files folder instead
            setup_done = get_config_value(Config.Crack.str(), Config.Crack.SetupComplete, "False").lower() == "true"
        case _:
            setup_done = False
    return setup_done