import os
from pathlib import Path
import sys


if getattr(sys, 'frozen', False):
    DEBUG = False
else:
    DEBUG = True
    
# Get user Roaming folder
if os.name == "nt":
    ROAMING = Path(os.getenv("APPDATA"))
else:
    ROAMING = Path.home() / ".config"

initial = False

script_version = "v6.0.0"

gv_account_name = "GameVault" # Default account name to use for specific "versions" of a game. users can change the default field
APP_NAME = "GVU"

INTERNAL_NAME = f"_{APP_NAME}"                  # _GVU
CONFIG_FILENAME = f"{APP_NAME.lower()}_config"  # GVU -> gvu
CONFIG_COPY_SUFFIX = "_copy_DO_NOT_DELETE"

# ----------------------------
# Paths
# ----------------------------
BASE_PATH                   = Path.cwd()
LOCALE_PATH                 = f"{INTERNAL_NAME}/locale/localization.json" if not DEBUG else "locale/localization.json"
CONFIG_DIR_PATH             = Path(f"{INTERNAL_NAME}/{APP_NAME} config") if not DEBUG else Path(f"{APP_NAME} config")       # _GVU/GVU config
GAMEVAULT_GAME_PATH         = BASE_PATH.parent                          # ex. (1)Random Game
GAMEVAULT_ROOT_PATH         = BASE_PATH.parent.parent.parent            # ex. GameVault -> Installations | Downloads
PERSISTENT_DATA_PATH        = GAMEVAULT_ROOT_PATH / "Persistent Data"   # Persistent Data directory will be made beside Installations, with sub folder containing GAMEVAULT_GAME_PATH

GAME_NAME                   = GAMEVAULT_GAME_PATH.name
PERSISTENT_DATA_GAME_PATH   = PERSISTENT_DATA_PATH / GAME_NAME
    
CONFIG_PATH                 = BASE_PATH / CONFIG_DIR_PATH / f"{CONFIG_FILENAME}.ini"                    # external config
CONFIG_COPY_PATH            = BASE_PATH / CONFIG_DIR_PATH / f"{CONFIG_FILENAME}{CONFIG_COPY_SUFFIX}.ini" # external config copy
GAMEVAULT_EXEC_CONFIG       = GAMEVAULT_GAME_PATH / "gamevault-exec"               # parent path's config file
ORIGINAL_FILES_PATH         = BASE_PATH / CONFIG_DIR_PATH / "original files"
CRACKED_FILES_PATH          = BASE_PATH / CONFIG_DIR_PATH / "cracked files"
GLOBAL_CONFIG               = ROAMING / APP_NAME / f"{CONFIG_FILENAME}_global.ini"      # contains data if OnlineFix or Goldberg has been setup, since they are one time global setups

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
