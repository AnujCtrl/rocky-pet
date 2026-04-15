import json
from pathlib import Path
from rocky_pet.settings import SettingsManager


def test_default_settings(tmp_path):
    mgr = SettingsManager(tmp_path / "settings.json")
    assert mgr.hotkey == "Ctrl+Shift+R"
    assert mgr.volume == 0.7
    assert mgr.first_run is True
    assert mgr.interaction_interval == 120


def test_save_and_load(tmp_path):
    path = tmp_path / "settings.json"
    mgr = SettingsManager(path)
    mgr.hotkey = "Ctrl+Alt+R"
    mgr.volume = 0.5
    mgr.first_run = False
    mgr.save()
    mgr2 = SettingsManager(path)
    assert mgr2.hotkey == "Ctrl+Alt+R"
    assert mgr2.volume == 0.5
    assert mgr2.first_run is False


def test_mark_first_run_complete(tmp_path):
    path = tmp_path / "settings.json"
    mgr = SettingsManager(path)
    assert mgr.first_run is True
    mgr.mark_first_run_complete()
    assert mgr.first_run is False
    mgr2 = SettingsManager(path)
    assert mgr2.first_run is False


def test_corrupt_file_uses_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("not json{{{")
    mgr = SettingsManager(path)
    assert mgr.hotkey == "Ctrl+Shift+R"


def test_missing_keys_use_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"hotkey": "Ctrl+F12"}))
    mgr = SettingsManager(path)
    assert mgr.hotkey == "Ctrl+F12"
    assert mgr.volume == 0.7
