# Some modified games might have their user data directly in the game folder itself, 
# we use symlinks to move it from their modified location to their original location
import os
from pathlib import Path
import shutil
from typing import Literal, TypeAlias
from config_loader import DEBUG, parse_tuple_list_string


setup_keys_literal: TypeAlias = Literal['Target', 'Destination', 'Type']
setup_dict_literal: TypeAlias = dict[setup_keys_literal, str]
def parse_move_link_input(content: str) -> list[setup_dict_literal]:
    keys = ('Target', 'Destination', 'Type')
    target_source_dict_list = parse_tuple_list_string(content, 3, keys)
    return target_source_dict_list

def move_source_and_link_dir(paths: list[setup_dict_literal], exist_ok: bool = False):
    if isinstance(paths, str):
        target_source_dict_list = parse_move_link_input(paths)
        move_source_and_link_dir(target_source_dict_list, exist_ok)
        return
    for pair in paths:
        source      = Path(os.path.expandvars(pair['Target'])).absolute()
        destination = Path(os.path.expandvars(pair['Destination'])).absolute()
        type = pair['Type']
        # Move
        source_exists = source.exists()
        destination_exists = destination.exists()
        if destination_exists:
            if source_exists and not source.is_symlink():
                # to do: make an interactive prompt to show both folders and choose what to do with both
                raise FileExistsError(f"Path exists on both paths: {source} and {destination}")
        else:
            if not source_exists:
                if type == "Directory":
                    source.mkdir(parents=True)
                elif type == "File":
                    source.touch()
                else:
                    raise SyntaxError(f"Incorrect type: {type}, must be 'Directory' or 'File'")

            shutil.move(source, destination)

        # change variable names for readability
        link = source
        source = destination
        # Link
        # if not source.exists():
        #     raise FileNotFoundError(f"{source}")
        if source.is_symlink():
            raise Exception(f"Source is a symlink, {source}")
        if link.exists():
            if link.is_symlink():
                if not exist_ok: raise FileExistsError(f"{link}")
            else: raise FileExistsError(f"Link path is an actual file: {link}")
        
        source_is_dir = type == "Directory"
        if DEBUG: return
        
        Path(link).symlink_to(source, source_is_dir)
        