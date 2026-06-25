"""Configuration — settings for File Manager AI."""
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".filemanager-ai"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "ollama_url": "http://127.0.0.1:11434",
    "model": "qwen2.5:7b",
    "show_hidden": False,
    "trash_enabled": True,
    "theme": "dark",
}


def load_config() -> dict:
    """Load config from file or create default."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """Save config to file."""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
