from config_loader import *
from util import clear_screen, copy_files_from_reference
import re
from InquirerPy import inquirer

def validate_paths():
    GLOBAL_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "False").lower() == "false"
    if not GAMEVAULT_EXEC_CONFIG.is_file() and no_gamevault_mode: 
        proceed = inquirer.confirm(message=lang["no_gamevault.prompts.not_in_gamevault.message"],
                                   instruction=lang["no_gamevault.prompts.not_in_gamevault.instruction"],
                                   long_instruction=lang["no_gamevault.prompts.not_in_gamevault.l_instruction"],
                            default=True).execute()
        clear_screen()
        if not proceed:
            raise FileNotFoundError(lang["validate.errors.gamevault_exec_missing"](custom_script_name=custom_script_name))
        setup_no_gamevault()
    
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "False").lower() == "true"
    if not no_gamevault_mode:
        # Get GameVault ID
        get_gamevault_game_ID()

    has_original = get_config_value(Config.Default.str(), Config.Default.NoOriginal, "False").lower() == "false"
    if has_original and not ORIGINAL_FILES_PATH.is_dir(): raise FileNotFoundError(lang["errors.original_files_missing"](custom_script_name=custom_script_name))
    if has_original and not CRACKED_FILES_PATH.is_dir(): raise FileNotFoundError(lang["errors.crack_files_missing"](custom_script_name=custom_script_name))

def get_gamevault_game_ID():
    been_set = get_config_value(Config.Default.str(), Config.Default.GameVaultGameID, "-1") != "-1"
    if been_set:
        return
    # Get ID from folder
    if (DEBUG):
        match = re.search(r"\((\d+)\)", "(10)Test Game")
    else:
        match = re.search(r"\((\d+)\)", GAMEVAULT_GAME_PATH.name)
    if not match.group(1):
        raise Exception(lang["validate.errors.gamevault_game_id"])
    set_config_values(Config.Default.str(), Config.Default.GameVaultGameID, match.group(1))

def setup_no_gamevault():
    global config
    # copy/backup original files
    required_files = {"steam_api64.dll", "steam_api.dll"}
    found_files = copy_files_from_reference(BASE_PATH, Path(gvu_config_dir + "/cracked files"), Path(gvu_config_dir + "/original files"))
    if not found_files & required_files:
        raise FileNotFoundError(lang["no_gamevault.errors.not_found_steam_api"])
    
    # replace old config in case it was used by an old user
    shutil.copy2(CONFIG_COPY_PATH, CONFIG_PATH)
    config = ConfigObj(str(CONFIG_PATH))

    # set config of "no original" to false regardless of value (so version switcher shows up + original was already copied)
    set_config_values(Config.Default.str(), Config.Default.NoOriginal, "False")

    # finish setup
    set_config_values(Config.Other.str(), Config.Other.NoGameVaultMode, "True")
