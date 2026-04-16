from pathlib import Path
import shutil
from typing import Literal
from config_loader import BASE_PATH, ORIGINAL_FILES_PATH, CRACK_FILES_PATH, Config, set_config_values, lang
from util import pause
from logger import console

def change_version(version: Literal["Original", "Pirated"]):
    base_path = Path(BASE_PATH)
    folder1 = Path(ORIGINAL_FILES_PATH)
    folder2 = Path(CRACK_FILES_PATH)
    if version == "Original":
        source_folder, delete_folder = folder1, folder2
    elif version == "Pirated":
        source_folder, delete_folder = folder2, folder1
    else:
        console.print(lang["change_version.invalid_version_choice"])
        return

    # --- Recursively delete matching files in BASE_PATH ---
    if delete_folder.exists():
        for file_path in delete_folder.rglob("*"):
            if file_path.is_file():
                # Compute relative path from delete_folder
                rel_path = file_path.relative_to(delete_folder)
                # Concat with base path (game folder) to mimic
                target_file = base_path / rel_path
                if target_file.exists() and target_file.is_file():
                    target_file.unlink()
                    console.print(f"Deleted {target_file}")

    # --- Copy everything from source_folder into BASE_PATH ---
    if source_folder.exists():
        for file_path in source_folder.rglob("*"):
            if file_path.is_file():
                rel_path = file_path.relative_to(source_folder)
                target_file = base_path / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, target_file)
                console.print(f"Copied {file_path} to {target_file}")

    set_config_values(Config.Default.str(), Config.Default.GameVersion, version)
    console.print()
    console.print(f"Switched to {version}")
    pause()