from pathlib import Path
import subprocess

from config.config import APP_NAME, INTERNAL_NAME, LOCALE_PATH, ORIGINAL_FILES_PATH, CRACKED_FILES_PATH, CONFIG_DIR_PATH, CONFIG_COPY_PATH

subprocess.run([
    "pyinstaller",
    "-D",
    "-n", APP_NAME,
    "--contents-directory", INTERNAL_NAME,
    "--uac-admin",
    "--add-data", f"{LOCALE_PATH}:locale",
    "--add-data", f"{CONFIG_COPY_PATH}:{APP_NAME} config",
    "main.py",
], check=True)


# Place empty dirs after PyInstaller finishes
output_dir = Path("dist") / APP_NAME / INTERNAL_NAME / CONFIG_DIR_PATH

for directory in [
    output_dir / ORIGINAL_FILES_PATH.name,
    output_dir / CRACKED_FILES_PATH.name
]:
    directory.mkdir(parents=True, exist_ok=True)