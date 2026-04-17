from config_loader import *

def validate_paths():
    no_gamevault_mode = get_config_value(Config.Other.str(), Config.Other.NoGameVaultMode, "False").lower() == "false"
    if not GAMEVAULT_EXEC_CONFIG.is_file() and no_gamevault_mode: 
        proceed = inquirer.confirm(message=lang["no_gamevault.prompts.not_in_gamevault.message"],
                                   instruction=lang["no_gamevault.prompts.not_in_gamevault.instruction"],
                                   long_instruction=lang["no_gamevault.prompts.not_in_gamevault.l_instruction"],
                            default=True).execute()
        if not proceed:
            raise FileNotFoundError(lang["errors.gamevault_exec_missing"](custom_script_name=custom_script_name))
        set_config_values(Config.Other.str(), Config.Other.NoGameVaultMode, "True")

    has_original = get_config_value(Config.Default.str(), Config.Default.NoOriginal, "False").lower() == "false"
    if has_original and not ORIGINAL_FILES_PATH.is_dir(): raise FileNotFoundError(lang["errors.original_files_missing"](custom_script_name=custom_script_name))
    if has_original and not CRACKED_FILES_PATH.is_dir(): raise FileNotFoundError(lang["errors.crack_files_missing"](custom_script_name=custom_script_name))