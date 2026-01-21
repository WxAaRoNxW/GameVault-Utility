from dataclasses import dataclass
from configobj import ConfigObj

from config_loader import GLOBAL_CONFIG

# Config Schematic
@dataclass(frozen=True)
class GlobalConfig:
    @dataclass(frozen=True)
    class Setup:
        OnlineFix: str = "OnlineFix"
        Goldberg: str = "Goldberg"
        Goldberg_Old: str = "Goldberg Old"

        def str():
            return "SETUP COMPLETE"
        

global_config = ConfigObj(str(GLOBAL_CONFIG))
def set_global_config_value(section: str, key: str, value: str):
    if section not in global_config:
        global_config[section] = {}
    global_config[section][key] = value
    global_config.write()

def get_global_config_value(section: str, key: str, default: str):
    try:
        return global_config[section].get(key, default)
    except KeyError:
        return default