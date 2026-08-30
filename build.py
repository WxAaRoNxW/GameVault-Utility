import subprocess

from config.config import custom_script_name, internals_name, LOCALE_PATH

subprocess.run([
    "pyinstaller",
    "-D",
    "-n", custom_script_name,
    "--contents-directory", internals_name,
    "--uac-admin",
    "--add-data", f"{LOCALE_PATH}:locale",
    "main.py",
], check=True)
