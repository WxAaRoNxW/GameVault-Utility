from pathlib import Path

from config_loader import GAMEVAULT_EXEC_CONFIG

def set_executable(path: Path):
    data = {}

    # Read
    with GAMEVAULT_EXEC_CONFIG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key] = value

    # Modify
    data["Executable"] = str(path)

    # Write back
    with GAMEVAULT_EXEC_CONFIG.open("w", encoding="utf-8") as f:
        for key, value in data.items():
            f.write(f"{key}={value}\n")

#def set_gamevault_id(game_dir_name: str):
#   