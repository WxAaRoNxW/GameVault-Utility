# Some modified games might have their user data directly in the game folder itself, 
# we use symlinks to move it from their modified location to their original location
import os
from pathlib import Path
import shutil
from typing import Literal, TypeAlias
from config_loader import DEBUG, GAME_NAME, GAMEVAULT_GAME_PATH, PERSISTENT_DATA_GAME_PATH, parse_tuple_list_string
from lang import lang

setup_keys_literal: TypeAlias = Literal['Target', 'Destination', 'Type']
setup_dict_literal: TypeAlias = dict[setup_keys_literal, str]
def parse_move_link_input(content: str) -> list[setup_dict_literal]:
    keys = ('Target', 'Destination', 'Type')
    target_source_dict_list = parse_tuple_list_string(content, 3, keys)
    return target_source_dict_list

def move_source_and_link_dir(paths: list[setup_dict_literal], exist_ok: bool = False):
    for pair in paths:
        source      = Path(os.path.expandvars(format_path(pair['Target']))).absolute()
        destination = Path(os.path.expandvars(format_path(pair['Destination']))).absolute()
        type = pair['Type']
        # Move
        source_exists = source.exists()
        destination_exists = destination.exists()
        if destination_exists:
            if source_exists and not source.is_symlink():
                # to do: make an interactive prompt to show both folders and choose what to do with both
                raise FileExistsError(lang["errors.path_exists_both"](source=str(source), destination=str(destination)))
        else:
            if not source_exists:
                if type == "Directory":
                    source.mkdir(parents=True)
                elif type == "File":
                    source.touch()
                else:
                    raise SyntaxError(lang["errors.invalid_link_type"](type=type))

            shutil.move(source, destination)

        # change variable names for readability
        link = source
        source = destination
        # Link
        # if not source.exists():
        #     raise FileNotFoundError(f"{source}")
        if source.is_symlink():
            raise Exception(lang["errors.source_is_symlink"](source=str(source)))
        if link.exists():
            if link.is_symlink():
                if not exist_ok: raise FileExistsError(lang["errors.link_already_exists"](link=str(link)))
            else: raise FileExistsError(lang["errors.link_is_actual_file"](link=str(link)))
        
        source_is_dir = type == "Directory"
        if DEBUG: return
        
        Path(link).symlink_to(source, source_is_dir)

def format_path(path: str):
    keywords = {
        "game_name": GAME_NAME,
        "game_persistent_data_path": PERSISTENT_DATA_GAME_PATH
    }
    formatted_path = path.format(**keywords)
    return formatted_path