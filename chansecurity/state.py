import json
import os
from pathlib import Path

STATE_DIR = Path.home() / ".chansecurity"
STATE_FILE = STATE_DIR / "state.json"
PID_FILE = STATE_DIR / "daemon.pid"

def ensure_dir():
    STATE_DIR.mkdir(parents=True, exist_ok=True)

def write_state(data: dict):
    ensure_dir()
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, STATE_FILE)

def read_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def write_pid():
    ensure_dir()
    PID_FILE.write_text(str(os.getpid()))

def read_pid():
    try:
        return int(PID_FILE.read_text().strip())
    except (FileNotFoundError, ValueError):
        return None

def clear_pid():
    PID_FILE.unlink(missing_ok=True)

def is_daemon_alive():
    pid = read_pid()
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        clear_pid()
        return False
