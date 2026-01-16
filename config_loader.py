from dataclasses import dataclass
import shutil
from configobj import ConfigObj

from util import get_exe_path, pause
from logger import console

gv_name = "GameVault"
gvu_config_dir = "_GVU/GVU config"
custom_script_name = "GVU"
custom_script_filename = "gvu_config"
custom_script_copy_append = "_copy_DO_NOT_DELETE"

# ----------------------------
# Paths
# ----------------------------
BASE_PATH               = get_exe_path().parent
CONFIG_PATH             = BASE_PATH / gvu_config_dir / f"{custom_script_filename}.ini"                    # external config
CONFIG_COPY_PATH        = BASE_PATH / gvu_config_dir / f"{custom_script_filename}{custom_script_copy_append}.ini" # external config copy
GAMEVAULT_EXEC_CONFIG   = BASE_PATH.parent / "gamevault-exec"               # parent path's config file
ORIGINAL_FILES_PATH     = BASE_PATH / gvu_config_dir / "_original files"
CRACK_FILES_PATH        = BASE_PATH / gvu_config_dir / "_crack files"
GLOBAL_CONFIG           = BASE_PATH.parent.parent / f"{custom_script_filename}_global.ini"      # contains data if OnlineFix or Goldberg has been setup, since they are one time global setups

def validate_paths():
    try:
        if not GAMEVAULT_EXEC_CONFIG.is_file(): raise FileNotFoundError(f"gamevault-exec missing, is the {custom_script_name} script in the right path?")
        if not ORIGINAL_FILES_PATH.is_dir(): raise FileNotFoundError(f"'_original files' folder missing, is this a {custom_script_name} compatible game?")
        if not CRACK_FILES_PATH.is_dir(): raise FileNotFoundError(f"'_crack files' folder missing, is this a {custom_script_name} compatible game?")
        if not CONFIG_COPY_PATH.is_file():
            if CONFIG_PATH.is_file(): 
                console.print(f"'{custom_script_filename}{custom_script_copy_append}.ini' is missing, but still functional, ask GameVault Admin for repair file")
                pause(clear=True)
            else:
                raise FileNotFoundError(f"'{custom_script_filename}{custom_script_copy_append}.ini' is missing, ask GameVault Admin for repair file")
        if not CONFIG_PATH.is_file(): # copy if main config is missing
            shutil.copy2(CONFIG_COPY_PATH, CONFIG_PATH)
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

# Config Schematic
@dataclass(frozen=True)
class Config:
    @dataclass(frozen=True)
    class Default:
        Executable: str = "Executable"
        GameVersion: str = "GameVersion"
        DontAskAgain: str = "DontAskAgain"

        def str():
            return "DEFAULT"
    @dataclass(frozen=True)
    class Crack:
        Type: str = "Type"
        SetupComplete: str = "SetupComplete"
        
        def str():
            return "CRACK"

# ----------------------------
# Load external config
# ----------------------------

# Helper function to get value safely
def get_config_value(section, key, default=""):
    try:
        return config[section].get(key, default)
    except KeyError:
        return default

def set_config_values(section, key, value):
    # Optionally mark as done in external config
    if section not in config:
        config[section] = {}
    config[section][key] = value
    config.write()

validate_paths()
config = ConfigObj(str(CONFIG_PATH))