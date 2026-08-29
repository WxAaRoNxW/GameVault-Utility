from dataclasses import dataclass
import shutil
import sys
from configobj import ConfigObj

from config import *
from util import pause
from logger import console
from lang import lang

try:
    if not CONFIG_COPY_PATH.is_file():
        if CONFIG_PATH.is_file(): 
            console.print(lang["messages.config_missing"](custom_script_filename=custom_script_filename, custom_script_copy_append=custom_script_copy_append))
            pause(clear=True)
        else:
            raise FileNotFoundError(lang["errors.config_missing_backup"](custom_script_filename=custom_script_filename, custom_script_copy_append=custom_script_copy_append))
    if not CONFIG_PATH.is_file(): # copy if main config is missing
        initial = True
        shutil.copy2(CONFIG_COPY_PATH, CONFIG_PATH)
except Exception as e:
    import traceback
    traceback.print_exc()
    pause("\nPress Enter to exit...")
    sys.exit(1)
config = ConfigObj(str(CONFIG_PATH))

# Config Schematic
@dataclass(frozen=True)
class Config:
    @dataclass(frozen=True)
    class Default:
        Executable: str = "Executable"
        LaunchParameter: str = "LaunchParameter"
        GameVersion: str = "GameVersion"
        GameVaultGameID = "GameVaultGameID" # To launch the game through gamevault url
        SteamAppID: str = "SteamAppID"
        DontAskAgain: str = "DontAskAgain"
        NoOriginal: str = "NoOriginal"

        def str():
            return "DEFAULT"
    @dataclass(frozen=True)
    class Crack:
        Type: str = "Type"
        SetupComplete: str = "SetupComplete"
        NoSetup: str = "NoSetup"
        
        def str():
            return "CRACK"
    @dataclass(frozen=True)
    class Setup:
        FileEdits: str = "FileEdits"
        PathMoveLinking: str = "PathMoveLinking"
        PathMoveLinkingComplete: str = "PathMoveLinkingComplete"
        def str():
            return "SETUP"
    @dataclass(frozen=True)
    class Other:
        NoGameVaultMode: str = "NoGameVaultMode"
        def str():
            return "OTHER"

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

def parse_tuple_list_string(content: str, required_length: int, keys: tuple) -> list[dict[str, str]]:
    if required_length == 0:
        return False
    if content == "":
        raise Exception(lang["errors.string_empty"])
    content_list = content.strip().split(",,") 

    content_tuple_list = []
    for line in content_list:
        line_split = []
        for element in line.split(";;"):
            line_split.append(element.strip())
        content_tuple_list.append(line_split)
    
    # Validate tuple length
    if not all(len(t) == required_length for t in content_tuple_list):
        raise ValueError(lang["errors.tuple_validation_failed"](required_length=required_length))
    
    # result = [dict(zip(keys, tupleVal)) for tupleVal in points]
    result: list[dict[str, str]] = []
    for tupleVal in content_tuple_list:
        pairsList = zip(keys, tupleVal) # 2 tuples will be paired together
        dict_pairs = dict(pairsList)
        result.append(dict_pairs)

    return result

config: ConfigObj