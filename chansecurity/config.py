import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".chansecurity"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "gmail_address": "",
    "gmail_app_password": "",
    "email_to": "",
    "email_locked": False,
    "tiers": {
        "cpu": [[80, 50, 3600], [90, 50, 900], [100, 50, 600]],
        "ram": [[80, 50, 3600], [90, 50, 900], [100, 50, 600]],
        "network": [[80, 50, 3600], [90, 50, 900], [100, 50, 600]],
    },
}

def load_config():
    if not CONFIG_FILE.exists():
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        merged = dict(DEFAULT_CONFIG)
        merged.update(data)
        merged["tiers"] = {**DEFAULT_CONFIG["tiers"], **data.get("tiers", {})}
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)

def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def is_configured(config):
    return bool(config["gmail_address"] and config["gmail_app_password"] and config["email_to"])