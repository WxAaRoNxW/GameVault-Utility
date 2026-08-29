from pathlib import Path

from config.config_loader import GAMEVAULT_EXEC_CONFIG

class GVExecConfig:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = {}
        self._load()

    def _load(self):
        """Read config file into dict"""
        self.data.clear()
        if not self.config_path.exists():
            return

        with self.config_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                self.data[key] = value

    def save(self):
        """Write dict back to file"""
        with self.config_path.open("w", encoding="utf-8") as f:
            for key, value in self.data.items():
                f.write(f"{key}={value}\n")

    def set_executable(self, path: Path):
        self.data["Executable"] = str(path)
        self.save()

    def set_launch_parameter(self, param: str):
        self.data["LaunchParameter"] = param.strip()
        self.save()

    def get_executable(self) -> Path | None:
        val = self.data.get("Executable")
        return Path(val) if val else None

    def get_launch_parameter(self) -> str | None:
        return self.data.get("LaunchParameter")
#def set_gamevault_id(game_dir_name: str):
#   