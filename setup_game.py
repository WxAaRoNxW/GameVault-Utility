from enum import Enum
import os
from pathlib import Path
from typing import Literal, TypeAlias
import webbrowser

from configobj import ConfigObj
from config_loader import Config, get_config_value, parse_tuple_list_string, set_config_values, gv_name
from config_loader import ROAMING, Config, get_config_value, parse_tuple_list_string, set_config_values, gv_name
from global_config import GlobalConfig, get_global_config_value, set_global_config_value
from prompt_key_actions import get_l_instruction_suffix, get_keybindings
from prompt_validator import validate_prompt, validate_steam_id
from symlink import move_source_and_link_dir
from util import clear_screen, clear_input_buffer, pause, prompt_yes_no, sleep
from logger import console
from InquirerPy import inquirer

class CRACK_TYPES(Enum):
    OnlineFix = 0
    Goldberg = 1
    RUNE = 2
    Other = 3
    NoSetup = 4

def mark_done(setup_type: CRACK_TYPES):
    match setup_type:
        case CRACK_TYPES.OnlineFix:
            set_global_config_value(GlobalConfig.Setup.str(), GlobalConfig.Setup.OnlineFix, "True")
        case CRACK_TYPES.Goldberg:
            set_global_config_value(GlobalConfig.Setup.str(), GlobalConfig.Setup.Goldberg, "True")
        case CRACK_TYPES.RUNE | CRACK_TYPES.Other:
            set_config_values(Config.Crack.str(), Config.Crack.SetupComplete, "True")
        case CRACK_TYPES.NoSetup:
            return
        case _:
            console.print("Can't identify crack type, contact GameVault admin.")
            pause(clear=True)

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

        case CRACK_TYPES.RUNE | CRACK_TYPES.Other:
            # just get config value in _crack files folder instead
            setup_done = get_config_value(Config.Crack.str(), Config.Crack.SetupComplete, "False").lower() == "true"
        case CRACK_TYPES.NoSetup:
            setup_done = True
        case _:
            setup_done = False
    return setup_done

# 3. One-time global setup
def one_time_setup():
    # Get crack type
    setup_type = CRACK_TYPES[get_config_value(Config.Crack.str(), Config.Crack.Type, "N/A")]
    pathlink_string = get_config_value(Config.Setup.str(), Config.Setup.PathMoveLinking, '')
    if pathlink_string.strip() != '':
        move_source_and_link_dir(pathlink_string, exist_ok=True)

    # Run crack type's method using switch case
    match setup_type:
        case CRACK_TYPES.OnlineFix:
            onlinefix_setup()
        case CRACK_TYPES.Goldberg:
            goldberg_old_setup()
        case CRACK_TYPES.RUNE:
            rune_setup()
        case CRACK_TYPES.Other:
            other_setup()
        case _:
            console.print("Can't identify crack type, contact GameVault admin.")
            pause(clear=True)

def onlinefix_setup():
    proceed = inquirer.confirm(message="Have you ever added Spacewar to your steam library in the past by installing and removing it?", 
                               default=False).execute()
    if proceed:
        console.print("Nothing to do, setup complete.")
        mark_done(CRACK_TYPES.OnlineFix)
        return
    
    console.print("Steam will pop-up to ask you to install Spacewar (to add to your library)")
    console.print("You can immediately cancel/remove as soon as you PRESS INSTALL")
    sleep(5)
    webbrowser.open("steam://install/480")
    console.print("If the install menu doesn't show up, make sure you've logged-in or selected an account you'll use on steam.")
    console.print("Once done, setup is complete for EVERY OnlineFix games for THIS Steam account")
    pause()
    mark_done(CRACK_TYPES.OnlineFix)

setup_keys_literal: TypeAlias = Literal['Path', 'Message', 'Instructions', 'Long Instructions', 'Default', 'Key Action', 'Validator', 'Section', 'Key']
setup_dict_literal: TypeAlias = dict[setup_keys_literal, str]
def parse_setup_options() -> list[setup_dict_literal]:
    file_edits = get_config_value(Config.Setup.str(), Config.Setup.FileEdits, "").strip()
    prompt_dicts_list = parse_tuple_list_string(file_edits, 9, ("Path", "Message", 'Instructions', 'Long Instructions', 'Default', 'Key Action', 'Validator', "Section", "Key"))

    return prompt_dicts_list

def other_setup():
    try:
        prompt_dicts_list = parse_setup_options()
    except:
        raise Exception("Prompt empty even though setup exists.")

    for prompt_dict in prompt_dicts_list:
        config_other = ConfigObj(str(Path(os.path.expandvars(prompt_dict["Path"])).resolve()))
        
        default_value = config_other[prompt_dict["Section"]].get(
            prompt_dict["Key"], 
            "" if prompt_dict["Default"] == "None" else prompt_dict["Default"]
            )
        # if config_other[prompt_dict["Section"]].get(prompt_dict["Key"], ""):
        #     default_value = config_other[prompt_dict["Section"]].get(prompt_dict["Key"], "")
        # else:
        #     default_value = "" if prompt_dict["Default"] == "None" else prompt_dict["Default"]

        l_instruction = "" if prompt_dict["Long Instructions"] == "None" else prompt_dict["Long Instructions"]
        l_instruction = "\n".join([get_l_instruction_suffix(prompt_dict["Key Action"]), l_instruction]).strip()
        prompt = inquirer.text(message=prompt_dict["Message"],
                                      default=default_value,
                                      instruction= "" if prompt_dict["Instructions"] == "None" else prompt_dict["Instructions"],
                                      long_instruction=l_instruction,
                                      validate=validate_prompt(prompt_dict["Validator"])
                                      )
        get_keybindings(prompt=prompt, key_action=prompt_dict["Key Action"])
        user_id_input = prompt.execute()

        config_other[prompt_dict["Section"]][prompt_dict["Key"]] = user_id_input
        config_other.write()
        #Path(os.path.expandvars(prompt_dict["Path"])).resolve().write_text(user_id_input, encoding="utf-8")
    console.print(f"Setup complete!")
    pause(clear=True)
    mark_done(CRACK_TYPES.Other)

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

# Goldberg setup
def goldberg_old_setup():
    name_file = "account_name.txt"
    steam_id_file = "user_steam_id.txt"
    def modify_data(current_name, current_id):
        # Prompt user
        name_input = inquirer.text(message="Enter your name:", 
                      default=current_name,
                      instruction="This is what you'll be seen as in-game",
                      validate= lambda result: len(result) > 0
                      ).execute()

        console.print("A web page will open for you to find your Steam ID")
        sleep(2)
        webbrowser.open("https://steamid.xyz/")
        #while True:
        user_id_input = inquirer.text(message="Enter your Steam64 ID:", 
                                        default=current_id,
                                        long_instruction="Some games' save file are located in this Steam ID.\nBest to stick to one Steam ID or else you'll have to manually migrate your save files when you change midway.\nYou can choose a fake or your own, doesn't matter.",
                                        validate=validate_steam_id
                                        ).execute()
            
        # Write name.txt and id.txt
        (settings_folder / "account_name.txt").write_text(name_input, encoding="utf-8")
        (settings_folder / "user_steam_id.txt").write_text(user_id_input, encoding="utf-8")
        
        console.print(f"Setup complete for Goldberg in {settings_folder}")
        pause(clear=True)
        # Mark config complete
        mark_done(CRACK_TYPES.Goldberg)

    # Get user Roaming folder
    settings_folder = ROAMING / "Goldberg SteamEmu Saves" / "settings"
    settings_folder.mkdir(parents=True, exist_ok=True)
    settings_name_path = settings_folder / name_file
    settings_id_path = settings_folder / steam_id_file
    account_name: str = gv_name
    id_content: str = "76561197960265728"
    exists = False
    # Check if files exists and Show existing data
    name_exists = settings_name_path.is_file()
    id_exists = settings_id_path.is_file()
    if name_exists or id_exists:
        console.print("[yellow]You have an existing configuration from past pirated games that uses Goldberg.")
        exists = True
        if name_exists:
            account_name = settings_name_path.read_text(encoding="utf-8").strip()
            console.print(f"Current username is, {account_name}")
        if id_exists:
            id_content = settings_id_path.read_text(encoding="utf-8").strip()
            console.print(f"Current steam id is, {id_content}")

        # Prompt setup to modify if exists
        if exists:
            proceed = inquirer.confirm(message="Would you like to change this?...",
                                       instruction="Not proceeding will complete the setup.",
                                       default=True).execute()
            if not proceed: 
                mark_done(CRACK_TYPES.Goldberg)
                return
            modify_data(account_name, id_content)

    # Else prompt setup
    else:
        modify_data(account_name, id_content)
    
    clear_screen()
