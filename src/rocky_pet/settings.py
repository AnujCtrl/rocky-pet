import json
from pathlib import Path

DEFAULTS = {
    "hotkey": "Ctrl+Shift+R",
    "volume": 0.7,
    "first_run": True,
    "interaction_interval": 120,
}


class SettingsManager:
    def __init__(self, path: Path | None = None):
        if path is None:
            config_dir = Path.home() / ".rocky-pet"
            config_dir.mkdir(exist_ok=True)
            path = config_dir / "settings.json"
        self._path = path
        self._data: dict = dict(DEFAULTS)
        self._load()

    def _load(self):
        if self._path.exists():
            try:
                with open(self._path) as f:
                    saved = json.load(f)
                self._data.update(saved)
            except (json.JSONDecodeError, OSError):
                pass

    def save(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(self._data, f, indent=2)

    @property
    def hotkey(self) -> str:
        return self._data["hotkey"]

    @hotkey.setter
    def hotkey(self, value: str):
        self._data["hotkey"] = value

    @property
    def volume(self) -> float:
        return self._data["volume"]

    @volume.setter
    def volume(self, value: float):
        self._data["volume"] = max(0.0, min(1.0, value))

    @property
    def first_run(self) -> bool:
        return self._data["first_run"]

    @first_run.setter
    def first_run(self, value: bool):
        self._data["first_run"] = value

    @property
    def interaction_interval(self) -> int:
        return self._data["interaction_interval"]

    @interaction_interval.setter
    def interaction_interval(self, value: int):
        self._data["interaction_interval"] = max(30, value)

    def mark_first_run_complete(self):
        self.first_run = False
        self.save()
