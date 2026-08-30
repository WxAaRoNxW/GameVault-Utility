from config.config_loader import *
from util.util import clear_screen, copy_files_from_reference
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

    for directory in [
        ORIGINAL_FILES_PATH,
        CRACKED_FILES_PATH
    ]:
        directory.mkdir(parents=True, exist_ok=True)
        
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

def backup_original_files():
    orig_dir = ORIGINAL_FILES_PATH
    # Backup GVU original files
    has_original = get_config_value(Config.Default.str(), Config.Default.NoOriginal, "False").lower() == "false"
    if not has_original:
        return
    gvu_orig_dir = BASE_PATH / gvu_config_dir / "gvu original files"
    # Check if "gvu original files" exist
    if gvu_orig_dir.is_dir():
        return
    # Check if orig dir is not empty as a precaution
    if not any(orig_dir.iterdir()):
        return
    
    shutil.move(orig_dir, gvu_orig_dir)

def setup_no_gamevault():
    global config
    orig_dir = ORIGINAL_FILES_PATH
    crack_dir = CRACKED_FILES_PATH
    temp_dir = BASE_PATH / gvu_config_dir / "temp_original_files"

    # Copy files to temp location and get results to check if game is clean
    found_files, found_ref_files = copy_files_from_reference(BASE_PATH, crack_dir, temp_dir)

    # if true, means all files from crack are found in base_path, meaning there's no original files in base path, pre-cracked
    game_is_clean = found_files != found_ref_files
    if game_is_clean:
        # Only backup and move if game is clean
        backup_original_files()
        shutil.move(str(temp_dir), str(orig_dir))
        # copy/backup original files
        required_files = {"steam_api64.dll", "steam_api.dll"}
        stripped_found_files = {found_file.name for found_file in found_files}
        
        if not stripped_found_files & required_files:
            raise FileNotFoundError(lang["no_gamevault.errors.not_found_steam_api"])
    else:
        # Clean up temp directory if game is not clean
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    
    if not initial:
        # replace old config in case it was used by an old user
        shutil.copy2(CONFIG_COPY_PATH, CONFIG_PATH)
        config = ConfigObj(str(CONFIG_PATH))

    # set config of "no original" to false regardless of value (so version switcher shows up + original was already copied)
    set_config_values(Config.Default.str(), Config.Default.NoOriginal, "False")
    set_config_values(Config.Default.str(), Config.Default.GameVersion, "Original")

    # finish setup
    set_config_values(Config.Other.str(), Config.Other.NoGameVaultMode, "True")
