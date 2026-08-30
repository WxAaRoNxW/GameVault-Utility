from pathlib import Path
import subprocess

from config.config import custom_script_name, internals_name, LOCALE_PATH, ORIGINAL_FILES_PATH, CRACKED_FILES_PATH, gvu_config_dir, CONFIG_COPY_PATH

subprocess.run([
    "pyinstaller",
    "-D",
    "-n", custom_script_name,
    "--contents-directory", internals_name,
    "--uac-admin",
    "--add-data", f"{LOCALE_PATH}:locale",
    "--add-data", f"{CONFIG_COPY_PATH}:{custom_script_name} config",
    "main.py",
], check=True)


# Place empty dirs after PyInstaller finishes
output_dir = Path("dist") / custom_script_name / internals_name / gvu_config_dir

for directory in [
    output_dir / ORIGINAL_FILES_PATH.name,
    output_dir / CRACKED_FILES_PATH.name
]:
    directory.mkdir(parents=True, exist_ok=True)