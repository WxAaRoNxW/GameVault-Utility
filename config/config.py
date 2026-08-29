import os
from pathlib import Path
import sys


if getattr(sys, 'frozen', False):
    DEBUG = False
else:
    DEBUG = True

script_version = "v5.1.0"

gv_account_name = "GameVault"
custom_script_name = "GVU"

internals_name = f"_{custom_script_name}"                                   # _GVU
gvu_config_dir = Path(f"{internals_name}/{custom_script_name} config")      # _GVU/GVU config
custom_script_filename = f"{custom_script_name.lower()}_config"             # GVU -> gvu
custom_script_copy_append = "_copy_DO_NOT_DELETE"
initial = False

# ----------------------------
# Base Paths
# ----------------------------
LOCALE_PATH                 = f"{internals_name}/locale/localization.json" if not DEBUG else "locale/localization.json"
BASE_PATH                   = Path.cwd()
GAMEVAULT_GAME_PATH         = BASE_PATH.parent           # ex. (1)Random Game
GAMEVAULT_ROOT_PATH         = BASE_PATH.parent.parent.parent # ex. GameVault -> Installations | Downloads
PERSISTENT_DATA_PATH        = GAMEVAULT_ROOT_PATH / "Persistent Data"

GAME_NAME = GAMEVAULT_GAME_PATH.name
PERSISTENT_DATA_GAME_PATH   = PERSISTENT_DATA_PATH / GAME_NAME

# ----------------------------
# Paths
# ----------------------------
# Get user Roaming folder
if os.name == "nt":
    ROAMING = Path(os.getenv("APPDATA"))
else:
    ROAMING = Path.home() / ".config"
    
CONFIG_PATH                 = BASE_PATH / gvu_config_dir / f"{custom_script_filename}.ini"                    # external config
CONFIG_COPY_PATH            = BASE_PATH / gvu_config_dir / f"{custom_script_filename}{custom_script_copy_append}.ini" # external config copy
GAMEVAULT_EXEC_CONFIG       = GAMEVAULT_GAME_PATH / "gamevault-exec"               # parent path's config file
ORIGINAL_FILES_PATH         = BASE_PATH / gvu_config_dir / "original files"
CRACKED_FILES_PATH          = BASE_PATH / gvu_config_dir / "cracked files"
GLOBAL_CONFIG               = ROAMING / custom_script_name / f"{custom_script_filename}_global.ini"      # contains data if OnlineFix or Goldberg has been setup, since they are one time global setups

header_config = {
    "title": [
        {"text": "Game", "style": "game"},
        {"text": "{{gamemode}}", "style": "mode"},
        {"text": " Utility", "style": "util"},
        {"text": " - "},
        {"text": f"{script_version}", "style": "version"},
    ],
    "styles": {
        "": "bold underline",
        "game": "#4f46af",
        "util": "cyan",
        "version": "yellow",
    }
}
