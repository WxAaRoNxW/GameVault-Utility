from config_loader import *
from util import copy_files_from_reference

def validate_paths():
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "False").lower() == "false"
    if not GAMEVAULT_EXEC_CONFIG.is_file() and no_gamevault_mode: 
        proceed = inquirer.confirm(message=lang["no_gamevault.prompts.not_in_gamevault.message"],
                                   instruction=lang["no_gamevault.prompts.not_in_gamevault.instruction"],
                                   long_instruction=lang["no_gamevault.prompts.not_in_gamevault.l_instruction"],
                            default=True).execute()
        if not proceed:
            raise FileNotFoundError(lang["errors.gamevault_exec_missing"](custom_script_name=custom_script_name))
        setup_no_gamevault()
    has_original = get_config_value(Config.Default.str(), Config.Default.NoOriginal, "False").lower() == "false"
    if has_original and not ORIGINAL_FILES_PATH.is_dir(): raise FileNotFoundError(lang["errors.original_files_missing"](custom_script_name=custom_script_name))
    if has_original and not CRACKED_FILES_PATH.is_dir(): raise FileNotFoundError(lang["errors.crack_files_missing"](custom_script_name=custom_script_name))

def setup_no_gamevault():
    global config
    # copy/backup original files
    required_files = {"steam_api64.dll", "steam_api.dll"}
    found_files = copy_files_from_reference(BASE_PATH, Path(gvu_config_dir + "/cracked files"), Path(gvu_config_dir + "/original files"))
    if not found_files & required_files:
        raise FileNotFoundError("Unable to backup original steam api file, is this a steam game?")
    
    # replace old config in case it was used by an old user
    shutil.copy2(CONFIG_COPY_PATH, CONFIG_PATH)
    config = ConfigObj(str(CONFIG_PATH))

    # set config of "no original" to true regardless of value
    set_config_values(Config.Default.str(), Config.Default.NoOriginal, "True")

    # finish setup
    set_config_values(Config.Other.str(), Config.Other.NoGameVaultMode, "True")
